DROP VIEW IF EXISTS sm_oee_kpi;

CREATE VIEW sm_oee_kpi AS
WITH usage AS (
    SELECT
        machine_id,
        date(start_time) AS usage_date,
        SUM(runtime_minutes) AS total_runtime_minutes,
        SUM(downtime_minutes) AS total_downtime_minutes
    FROM fact_machine_usage
    GROUP BY machine_id, date(start_time)
),
downtime AS (
    SELECT
        machine_id,
        date(start_time) AS downtime_date,
        SUM(downtime_minutes) AS total_downtime_minutes
    FROM fact_machine_downtime
    GROUP BY machine_id, date(start_time)
)
SELECT
    u.machine_id,
    m.machine_code,
    u.usage_date AS kpi_date,
    u.total_runtime_minutes,
    COALESCE(d.total_downtime_minutes, u.total_downtime_minutes) AS total_downtime_minutes,
    (u.total_runtime_minutes
        + COALESCE(d.total_downtime_minutes, u.total_downtime_minutes)) AS total_minutes,
    CASE
        WHEN (u.total_runtime_minutes
              + COALESCE(d.total_downtime_minutes, u.total_downtime_minutes)) > 0
        THEN u.total_runtime_minutes * 1.0
             / (u.total_runtime_minutes
                + COALESCE(d.total_downtime_minutes, u.total_downtime_minutes))
        ELSE NULL
    END AS availability
    -- Performance and Quality can be added once throughput + good/scrap units are wired
FROM usage u
JOIN dim_machines m
    ON u.machine_id = m.machine_id
LEFT JOIN downtime d
    ON u.machine_id = d.machine_id
   AND u.usage_date = d.downtime_date;
