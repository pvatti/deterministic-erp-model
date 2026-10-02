DROP VIEW IF EXISTS sm_predictive_maintenance_kpi;

CREATE VIEW sm_predictive_maintenance_kpi AS
WITH daily AS (
    SELECT
        machine_id,
        site_id,
        date(start_time) AS kpi_date,
        SUM(runtime_minutes) AS runtime_minutes,
        SUM(downtime_minutes) AS downtime_minutes
    FROM fact_machine_usage
    GROUP BY machine_id, site_id, date(start_time)
),
failures AS (
    SELECT
        machine_id,
        site_id,
        date(start_time) AS kpi_date,
        COUNT(*) AS failure_events,
        SUM(downtime_minutes) AS failure_downtime
    FROM fact_machine_downtime
    GROUP BY machine_id, site_id, date(start_time)
),
rolling AS (
    SELECT
        d.machine_id,
        d.site_id,
        d.kpi_date,

        -- 7-day rolling windows
        (SELECT SUM(runtime_minutes)
         FROM daily d2
         WHERE d2.machine_id = d.machine_id
           AND d2.site_id = d.site_id
           AND d2.kpi_date BETWEEN date(d.kpi_date, '-7 days') AND d.kpi_date
        ) AS runtime_7d,

        (SELECT SUM(downtime_minutes)
         FROM daily d3
         WHERE d3.machine_id = d.machine_id
           AND d3.site_id = d.site_id
           AND d3.kpi_date BETWEEN date(d.kpi_date, '-7 days') AND d.kpi_date
        ) AS downtime_7d,

        (SELECT SUM(failure_events)
         FROM failures f2
         WHERE f2.machine_id = d.machine_id
           AND f2.site_id = d.site_id
           AND f2.kpi_date BETWEEN date(d.kpi_date, '-7 days') AND d.kpi_date
        ) AS failures_7d
    FROM daily d
)
SELECT
    r.kpi_date,
    r.site_id,
    s.site_code,
    r.machine_id,
    m.machine_code,

    -- Rolling windows
    r.runtime_7d,
    r.downtime_7d,
    r.failures_7d,

    -- Degradation trend (downtime increasing faster than runtime)
    CASE
        WHEN r.runtime_7d = 0 THEN NULL
        ELSE r.downtime_7d * 1.0 / r.runtime_7d
    END AS degradation_ratio,

    -- Failure probability (simple heuristic)
    CASE
        WHEN r.runtime_7d = 0 THEN NULL
        ELSE (r.failures_7d * 1.0) / (r.runtime_7d / 60.0)
    END AS failure_probability,

    -- Risk score (composite)
    (
        COALESCE(r.failures_7d, 0) * 0.4 +
        COALESCE(r.downtime_7d, 0) * 0.3 +
        COALESCE(r.downtime_7d * 1.0 / NULLIF(r.runtime_7d, 0), 0) * 0.3
    ) AS risk_score,

    -- Predicted MTBF (simple projection)
    CASE
        WHEN r.failures_7d = 0 THEN NULL
        ELSE r.runtime_7d * 1.0 / r.failures_7d
    END AS predicted_mtbf_minutes,

    -- Predicted failure date (runtime trend)
    CASE
        WHEN r.failures_7d = 0 THEN NULL
        ELSE date(r.kpi_date, '+' || CAST((r.runtime_7d * 1.0 / r.failures_7d) / 60 AS INTEGER) || ' days')
    END AS predicted_failure_date,

    -- Anomaly flag (downtime spike)
    CASE
        WHEN r.downtime_7d > (SELECT AVG(downtime_minutes) * 2
                              FROM daily d
                              WHERE d.machine_id = r.machine_id
                                AND d.site_id = r.site_id)
        THEN 1
        ELSE 0
    END AS anomaly_flag

FROM rolling r
JOIN dim_sites s ON r.site_id = s.site_id
JOIN dim_machines m ON r.machine_id = m.machine_id;
