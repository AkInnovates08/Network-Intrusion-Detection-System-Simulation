import React, { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  LineChart,
  Line,
} from "recharts";
import "./style.css";

const API = "http://127.0.0.1:8000";

const STATUS_OPTIONS = [
  "ALL",
  "NEW",
  "INVESTIGATING",
  "RESOLVED",
  "FALSE_POSITIVE",
];

const SEVERITY_OPTIONS = [
  "ALL",
  "INFO",
  "LOW",
  "MEDIUM",
  "HIGH",
  "CRITICAL",
];

const TIME_OPTIONS = [
  { value: "ALL", label: "All time" },
  { value: "1H", label: "Last 1 hour" },
  { value: "6H", label: "Last 6 hours" },
  { value: "24H", label: "Last 24 hours" },
];

function App() {
  const [page, setPage] = useState("dashboard");
  const [stats, setStats] = useState({});
  const [alerts, setAlerts] = useState([]);
  const [traffic, setTraffic] = useState([]);
  const [selectedAlert, setSelectedAlert] = useState(null);
  const [selectedFlow, setSelectedFlow] = useState(null);
  const [notes, setNotes] = useState([]);
  const [noteText, setNoteText] = useState("");
  const [loading, setLoading] = useState(true);
  const [detailLoading, setDetailLoading] = useState(false);
  const [apiError, setApiError] = useState("");
  const [lastUpdated, setLastUpdated] = useState(null);

  const [statusFilter, setStatusFilter] = useState("ALL");
  const [severityFilter, setSeverityFilter] = useState("ALL");
  const [protocolFilter, setProtocolFilter] = useState("ALL");
  const [alertTypeFilter, setAlertTypeFilter] = useState("ALL");
  const [timeFilter, setTimeFilter] = useState("ALL");
  const [search, setSearch] = useState("");

  const [actionMessage, setActionMessage] = useState("");
  const [actionError, setActionError] = useState("");

  const fetchJson = async (url, options = {}) => {
    const response = await fetch(url, options);

    if (!response.ok) {
      let message = `Request failed: ${response.status}`;
      try {
        const body = await response.json();
        message = body.detail || message;
      } catch {
        // Keep HTTP status message.
      }
      throw new Error(message);
    }

    return response.json();
  };

  const loadDashboard = async () => {
    try {
      setApiError("");

      const [statsData, alertsData, trafficData] = await Promise.all([
        fetchJson(`${API}/api/dashboard/stats`),
        fetchJson(`${API}/api/alerts?limit=1000`),
        fetchJson(`${API}/api/dashboard/traffic?limit=200`),
      ]);

      setStats(statsData);
      setAlerts(Array.isArray(alertsData) ? alertsData : []);
      setTraffic(Array.isArray(trafficData) ? trafficData : []);
      setLastUpdated(new Date());
      setLoading(false);
    } catch (error) {
      console.error("IDS API error:", error);
      setApiError(
        "Unable to connect to the Network IDS API. Make sure FastAPI is running on http://127.0.0.1:8000."
      );
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDashboard();
    const interval = setInterval(loadDashboard, 3000);
    return () => clearInterval(interval);
  }, []);

  const protocolOptions = useMemo(() => {
    return [
      "ALL",
      ...Array.from(
        new Set(alerts.map((item) => item.protocol).filter(Boolean))
      ).sort(),
    ];
  }, [alerts]);

  const alertTypeOptions = useMemo(() => {
    return [
      "ALL",
      ...Array.from(
        new Set(alerts.map((item) => item.alert_type).filter(Boolean))
      ).sort(),
    ];
  }, [alerts]);

  const filteredAlerts = useMemo(() => {
    const now = Date.now();

    let minimumTime = null;
    if (timeFilter === "1H") minimumTime = now - 60 * 60 * 1000;
    if (timeFilter === "6H") minimumTime = now - 6 * 60 * 60 * 1000;
    if (timeFilter === "24H") minimumTime = now - 24 * 60 * 60 * 1000;

    const query = search.trim().toLowerCase();

    return alerts.filter((alert) => {
      const matchesStatus =
        statusFilter === "ALL" || alert.status === statusFilter;

      const matchesSeverity =
        severityFilter === "ALL" || alert.severity === severityFilter;

      const matchesProtocol =
        protocolFilter === "ALL" || alert.protocol === protocolFilter;

      const matchesType =
        alertTypeFilter === "ALL" || alert.alert_type === alertTypeFilter;

      const createdTime = new Date(alert.created_at || alert.timestamp).getTime();
      const matchesTime =
        minimumTime === null ||
        (Number.isFinite(createdTime) && createdTime >= minimumTime);

      const searchable = [
        alert.alert_id,
        alert.source_ip,
        alert.destination_ip,
        alert.alert_type,
        alert.rule_id,
        alert.protocol,
      ]
        .filter(Boolean)
        .join(" ")
        .toLowerCase();

      const matchesSearch = !query || searchable.includes(query);

      return (
        matchesStatus &&
        matchesSeverity &&
        matchesProtocol &&
        matchesType &&
        matchesTime &&
        matchesSearch
      );
    });
  }, [
    alerts,
    statusFilter,
    severityFilter,
    protocolFilter,
    alertTypeFilter,
    timeFilter,
    search,
  ]);

  const severityData = ["INFO", "LOW", "MEDIUM", "HIGH", "CRITICAL"].map(
    (severity) => ({
      severity,
      count: alerts.filter((item) => item.severity === severity).length,
    })
  );

  const riskTimeline = useMemo(() => {
    return [...traffic]
      .reverse()
      .map((item, index) => ({
        index: index + 1,
        risk: Number(item.risk_score || 0),
      }));
  }, [traffic]);

  const openInvestigation = async (alert) => {
    setSelectedAlert(alert);
    setPage("investigation");
    setDetailLoading(true);
    setActionMessage("");
    setActionError("");

    try {
      const [alertData, flowData, noteData] = await Promise.all([
        fetchJson(`${API}/api/alerts/${alert.alert_id}`),
        fetchJson(`${API}/api/flows/${alert.flow_id}`),
        fetchJson(`${API}/api/alerts/${alert.alert_id}/notes`),
      ]);

      setSelectedAlert(alertData);
      setSelectedFlow(flowData);
      setNotes(Array.isArray(noteData) ? noteData : []);
    } catch (error) {
      console.error(error);
      setActionError(error.message);
    } finally {
      setDetailLoading(false);
    }
  };

  const updateAlertStatus = async (newStatus) => {
    if (!selectedAlert) return;

    try {
      setActionError("");
      setActionMessage("");

      await fetchJson(`${API}/api/alerts/${selectedAlert.alert_id}/status`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status: newStatus }),
      });

      setSelectedAlert((current) => ({
        ...current,
        status: newStatus,
      }));

      setActionMessage(`Alert status changed to ${newStatus}.`);
      await loadDashboard();
    } catch (error) {
      setActionError(error.message);
    }
  };

  const saveNote = async () => {
    if (!selectedAlert || !noteText.trim()) return;

    try {
      setActionError("");
      setActionMessage("");

      await fetchJson(`${API}/api/alerts/${selectedAlert.alert_id}/notes`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ note: noteText.trim() }),
      });

      const updatedNotes = await fetchJson(
        `${API}/api/alerts/${selectedAlert.alert_id}/notes`
      );

      setNotes(Array.isArray(updatedNotes) ? updatedNotes : []);
      setNoteText("");
      setActionMessage("Analyst note saved.");
    } catch (error) {
      setActionError(error.message);
    }
  };

  const resetFilters = () => {
    setStatusFilter("ALL");
    setSeverityFilter("ALL");
    setProtocolFilter("ALL");
    setAlertTypeFilter("ALL");
    setTimeFilter("ALL");
    setSearch("");
  };

  const showDashboard = () => {
    setPage("dashboard");
    setSelectedAlert(null);
    setSelectedFlow(null);
  };

  const showAlerts = () => {
    setPage("alerts");
  };

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand-block">
          <div className="brand-mark">IDS</div>
          <div>
            <strong>Network IDS</strong>
            <span>SOC Console</span>
          </div>
        </div>

        <nav className="nav-menu">
          <button
            className={page === "dashboard" ? "nav-item active" : "nav-item"}
            onClick={showDashboard}
          >
            <span>Overview</span>
            <small>Dashboard</small>
          </button>

          <button
            className={page === "alerts" ? "nav-item active" : "nav-item"}
            onClick={showAlerts}
          >
            <span>Alert Queue</span>
            <small>{alerts.length} alerts</small>
          </button>

          <button
            className={page === "investigation" ? "nav-item active" : "nav-item"}
            onClick={() => selectedAlert && setPage("investigation")}
            disabled={!selectedAlert}
          >
            <span>Investigation</span>
            <small>{selectedAlert ? selectedAlert.alert_id : "Select an alert"}</small>
          </button>
        </nav>

        <div className="sidebar-divider" />

        <div className="filter-title">
          <span>Investigation Filters</span>
          <button onClick={resetFilters}>Reset</button>
        </div>

        <label>
          Status
          <select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)}>
            {STATUS_OPTIONS.map((option) => (
              <option key={option} value={option}>
                {option === "ALL" ? "All" : option.replace("_", " ")}
              </option>
            ))}
          </select>
        </label>

        <label>
          Severity
          <select
            value={severityFilter}
            onChange={(e) => setSeverityFilter(e.target.value)}
          >
            {SEVERITY_OPTIONS.map((option) => (
              <option key={option} value={option}>
                {option === "ALL" ? "All" : option}
              </option>
            ))}
          </select>
        </label>

        <label>
          Protocol
          <select
            value={protocolFilter}
            onChange={(e) => setProtocolFilter(e.target.value)}
          >
            {protocolOptions.map((option) => (
              <option key={option} value={option}>
                {option === "ALL" ? "All" : option}
              </option>
            ))}
          </select>
        </label>

        <label>
          Alert Type
          <select
            value={alertTypeFilter}
            onChange={(e) => setAlertTypeFilter(e.target.value)}
          >
            {alertTypeOptions.map((option) => (
              <option key={option} value={option}>
                {option === "ALL" ? "All" : option}
              </option>
            ))}
          </select>
        </label>

        <label>
          Time Range
          <select value={timeFilter} onChange={(e) => setTimeFilter(e.target.value)}>
            {TIME_OPTIONS.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </label>

        <label>
          Search
          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Alert, IP, rule..."
          />
        </label>

        <div className="filter-summary">
          <strong>{filteredAlerts.length}</strong>
          <span>matching alerts</span>
        </div>

        <div className="lab-badge">LAB DATA ONLY</div>
      </aside>

      <main className="content">
        <header className="topbar">
          <div>
            <p className="eyebrow">SOC / DEFENSIVE SIMULATION</p>
            <h1>Network Intrusion Detection System</h1>
            <p className="subtitle">
              Synthetic network-flow monitoring, detection and incident investigation.
            </p>
          </div>

          <div className="connection-state">
            <span className={apiError ? "status-dot offline" : "status-dot"} />
            {apiError ? "API Offline" : "API Connected"}
          </div>
        </header>

        {apiError && (
          <section className="error-banner">
            <strong>Backend connection problem</strong>
            <span>{apiError}</span>
          </section>
        )}

        {actionMessage && <div className="success-banner">{actionMessage}</div>}
        {actionError && <div className="error-banner">{actionError}</div>}

        {loading && !apiError ? (
          <section className="panel loading-panel">Loading IDS telemetry...</section>
        ) : page === "investigation" && selectedAlert ? (
          <InvestigationPage
            alert={selectedAlert}
            flow={selectedFlow}
            notes={notes}
            noteText={noteText}
            setNoteText={setNoteText}
            loading={detailLoading}
            onBack={showAlerts}
            onStatusChange={updateAlertStatus}
            onSaveNote={saveNote}
          />
        ) : page === "alerts" ? (
          <AlertsPage
            alerts={filteredAlerts}
            onOpen={openInvestigation}
          />
        ) : (
          <DashboardPage
            stats={stats}
            severityData={severityData}
            riskTimeline={riskTimeline}
            alerts={filteredAlerts.slice(0, 12)}
            onOpen={openInvestigation}
            lastUpdated={lastUpdated}
          />
        )}
      </main>
    </div>
  );
}

function DashboardPage({
  stats,
  severityData,
  riskTimeline,
  alerts,
  onOpen,
  lastUpdated,
}) {
  const cards = [
    ["Total Flows", stats.total_flows ?? 0],
    ["Normal", stats.normal ?? 0],
    ["Suspicious", stats.suspicious ?? 0],
    ["Open Alerts", stats.open_alerts ?? 0],
    ["Critical", stats.critical ?? 0],
    ["Avg Risk", Number(stats.avg_risk ?? 0).toFixed(1)],
  ];

  return (
    <>
      <div className="page-heading">
        <div>
          <h2>Security Overview</h2>
          <p>Current synthetic network activity and alert posture.</p>
        </div>
        {lastUpdated && (
          <span className="updated-label">
            Updated {lastUpdated.toLocaleTimeString()}
          </span>
        )}
      </div>

      <section className="cards">
        {cards.map(([label, value]) => (
          <div className="card" key={label}>
            <small>{label}</small>
            <strong>{value}</strong>
          </div>
        ))}
      </section>

      <div className="chart-grid">
        <section className="panel">
          <div className="panel-heading">
            <div>
              <h3>Alerts by Severity</h3>
              <span>Current alert distribution</span>
            </div>
          </div>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={severityData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="severity" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" name="Alerts" />
            </BarChart>
          </ResponsiveContainer>
        </section>

        <section className="panel">
          <div className="panel-heading">
            <div>
              <h3>Risk Timeline</h3>
              <span>Recent flow risk scores</span>
            </div>
          </div>
          <ResponsiveContainer width="100%" height={280}>
            <LineChart data={riskTimeline}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="index" />
              <YAxis domain={[0, 100]} />
              <Tooltip />
              <Line type="monotone" dataKey="risk" name="Risk" />
            </LineChart>
          </ResponsiveContainer>
        </section>
      </div>

      <section className="panel">
        <div className="panel-heading">
          <div>
            <h3>Recent Alerts</h3>
            <span>Click an alert to open the investigation workspace.</span>
          </div>
        </div>
        <AlertTable alerts={alerts} onOpen={onOpen} />
      </section>
    </>
  );
}

function AlertsPage({ alerts, onOpen }) {
  return (
    <>
      <div className="page-heading">
        <div>
          <h2>Alert Queue</h2>
          <p>Review, filter and investigate security alerts.</p>
        </div>
        <div className="queue-count">{alerts.length} visible</div>
      </div>

      <section className="panel">
        <AlertTable alerts={alerts} onOpen={onOpen} />
      </section>
    </>
  );
}

function AlertTable({ alerts, onOpen }) {
  if (!alerts.length) {
    return (
      <div className="empty-state">
        <strong>No alerts match the current filters.</strong>
        <span>Change the filters in the Investigation Filters panel.</span>
      </div>
    );
  }

  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Alert</th>
            <th>Source</th>
            <th>Destination</th>
            <th>Type</th>
            <th>Severity</th>
            <th>Risk</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {alerts.map((alert) => (
            <tr key={alert.alert_id}>
              <td className="mono">{alert.alert_id}</td>
              <td>{alert.source_ip}</td>
              <td>{alert.destination_ip}</td>
              <td>{alert.alert_type}</td>
              <td>
                <SeverityBadge severity={alert.severity} />
              </td>
              <td className="risk-value">{alert.risk_score}</td>
              <td>
                <StatusBadge status={alert.status} />
              </td>
              <td>
                <button
                  className="table-action"
                  onClick={() => onOpen(alert)}
                >
                  Investigate
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function InvestigationPage({
  alert,
  flow,
  notes,
  noteText,
  setNoteText,
  loading,
  onBack,
  onStatusChange,
  onSaveNote,
}) {
  return (
    <>
      <div className="page-heading">
        <div>
          <button className="back-button" onClick={onBack}>
            ← Back to Alert Queue
          </button>
          <h2>Alert Investigation</h2>
          <p>Analyst workspace for reviewing a detected security event.</p>
        </div>
        <StatusBadge status={alert.status} />
      </div>

      {loading ? (
        <section className="panel loading-panel">Loading investigation...</section>
      ) : (
        <>
          <section className="investigation-header panel">
            <div>
              <span className="eyebrow">ALERT ID</span>
              <h3>{alert.alert_id}</h3>
              <p>{alert.description}</p>
            </div>
            <div className="risk-box">
              <span>Risk Score</span>
              <strong>{alert.risk_score}/100</strong>
              <SeverityBadge severity={alert.severity} />
            </div>
          </section>

          <div className="investigation-grid">
            <section className="panel">
              <h3>Alert Details</h3>
              <DetailGrid
                items={[
                  ["Alert ID", alert.alert_id],
                  ["Created", formatDate(alert.created_at)],
                  ["Alert Type", alert.alert_type],
                  ["Rule ID", alert.rule_id],
                  ["Severity", alert.severity],
                  ["Status", alert.status],
                  ["Anomaly Score", alert.anomaly_score ?? "N/A"],
                  ["ML Score", alert.ml_score ?? "Disabled"],
                ]}
              />
            </section>

            <section className="panel">
              <h3>Network Context</h3>
              <DetailGrid
                items={[
                  ["Source IP", alert.source_ip],
                  ["Source Port", alert.source_port],
                  ["Destination IP", alert.destination_ip],
                  ["Destination Port", alert.destination_port],
                  ["Protocol", alert.protocol],
                  ["Flow ID", alert.flow_id],
                  ["Classification", flow?.classification || "N/A"],
                  ["Flow Risk", flow?.risk_score ?? "N/A"],
                ]}
              />
            </section>
          </div>

          <section className="panel">
            <h3>Traffic Statistics</h3>
            <div className="mini-cards">
              <MiniCard label="Packets" value={flow?.packet_count ?? "N/A"} />
              <MiniCard label="Bytes" value={flow?.byte_count ?? "N/A"} />
              <MiniCard label="Duration" value={flow?.duration ?? "N/A"} />
              <MiniCard label="Connections" value={flow?.connection_count ?? "N/A"} />
              <MiniCard
                label="Failed Connections"
                value={flow?.failed_connection_count ?? "N/A"}
              />
              <MiniCard label="Protocol" value={flow?.protocol ?? "N/A"} />
            </div>
          </section>

          <div className="investigation-grid">
            <section className="panel">
              <h3>Investigation Guidance</h3>
              <ul className="guidance-list">
                <li>Review related security and application logs.</li>
                <li>Determine whether the source is known and expected.</li>
                <li>Compare the activity against historical baselines.</li>
                <li>Review authentication records where authorized.</li>
                <li>Review firewall and endpoint telemetry where authorized.</li>
                <li>Determine whether the behavior has a legitimate business reason.</li>
              </ul>
            </section>

            <section className="panel">
              <h3>Matched Detection</h3>
              <div className="detection-callout">
                <span>{alert.rule_id}</span>
                <strong>{alert.alert_type}</strong>
                <p>{alert.description}</p>
              </div>
            </section>
          </div>

          <section className="panel">
            <h3>Incident Management</h3>
            <div className="status-actions">
              <button onClick={() => onStatusChange("NEW")}>
                Mark New
              </button>
              <button onClick={() => onStatusChange("INVESTIGATING")}>
                Start Investigation
              </button>
              <button onClick={() => onStatusChange("RESOLVED")}>
                Resolve
              </button>
              <button onClick={() => onStatusChange("FALSE_POSITIVE")}>
                False Positive
              </button>
            </div>
          </section>

          <section className="panel">
            <h3>Analyst Notes</h3>
            <textarea
              value={noteText}
              onChange={(event) => setNoteText(event.target.value)}
              placeholder="Document your investigation findings..."
              rows={5}
            />
            <button className="primary-button" onClick={onSaveNote}>
              Save Analyst Note
            </button>

            <div className="notes-list">
              {notes.length === 0 ? (
                <p className="muted">No analyst notes yet.</p>
              ) : (
                notes.map((note) => (
                  <article className="note-card" key={note.note_id}>
                    <div>
                      <strong>Analyst Note</strong>
                      <span>{formatDate(note.created_at)}</span>
                    </div>
                    <p>{note.note}</p>
                  </article>
                ))
              )}
            </div>
          </section>
        </>
      )}
    </>
  );
}

function DetailGrid({ items }) {
  return (
    <div className="detail-grid">
      {items.map(([label, value]) => (
        <div className="detail-item" key={label}>
          <span>{label}</span>
          <strong>{value ?? "N/A"}</strong>
        </div>
      ))}
    </div>
  );
}

function MiniCard({ label, value }) {
  return (
    <div className="mini-card">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function SeverityBadge({ severity }) {
  return (
    <span className={`severity severity-${String(severity || "INFO").toLowerCase()}`}>
      {severity || "INFO"}
    </span>
  );
}

function StatusBadge({ status }) {
  return (
    <span className={`status status-${String(status || "NEW").toLowerCase()}`}>
      {String(status || "NEW").replace("_", " ")}
    </span>
  );
}

function formatDate(value) {
  if (!value) return "N/A";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return date.toLocaleString();
}

createRoot(document.getElementById("root")).render(<App />);
