DROP VIEW IF EXISTS sm_machine_reliability_kpi;

CREATE VIEW sm_machine_reliability_kpi AS
WITH usage AS (
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
        SUM(downtime_minutes) AS total_failure_downtime
    FROM fact_machine_downtime
    GROUP BY machine_id, site_id, date(start_time)
)
SELECT
    u.kpi_date,
    u.site_id,
    s.site_code,
    u.machine_id,
    m.machine_code,

    -- Raw usage
    u.runtime_minutes,
    u.downtime_minutes,

    -- Failure events
    COALESCE(f.failure_events, 0) AS failure_events,
    COALESCE(f.total_failure_downtime, 0) AS failure_downtime_minutes,

    -- Uptime %
    CASE
        WHEN (u.runtime_minutes + u.downtime_minutes) = 0 THEN NULL
        ELSE u.runtime_minutes * 1.0 /
             (u.runtime_minutes + u.downtime_minutes)
    END AS uptime_pct,

    -- MTBF (Mean Time Between Failures)
    CASE
        WHEN COALESCE(f.failure_events, 0) = 0 THEN NULL
        ELSE u.runtime_minutes * 1.0 / f.failure_events
    END AS mtbf_minutes,

    -- MTTR (Mean Time To Repair)
    CASE
        WHEN COALESCE(f.failure_events, 0) = 0 THEN NULL
        ELSE f.total_failure_downtime * 1.0 / f.failure_events
    END AS mttr_minutes,

    -- Failure Rate (failures per runtime hour)
    CASE
        WHEN u.runtime_minutes = 0 THEN NULL
        ELSE f.failure_events * 60.0 / u.runtime_minutes
    END AS failure_rate_per_hour,

    -- Reliability Score (simple composite)
    CASE
        WHEN (u.runtime_minutes + u.downtime_minutes) = 0 THEN NULL
        ELSE
            (u.runtime_minutes * 1.0 /
             (u.runtime_minutes + u.downtime_minutes))  -- uptime
            *
            (1 - (COALESCE(f.failure_events, 0) * 1.0 / 10.0)) -- failure penalty
    END AS reliability_score

FROM usage u
JOIN dim_sites s ON u.site_id = s.site_id
JOIN dim_machines m ON u.machine_id = m.machine_id
LEFT JOIN failures f
    ON u.machine_id = f.machine_id
   AND u.site_id = f.site_id
   AND u.kpi_date = f.kpi_date;
