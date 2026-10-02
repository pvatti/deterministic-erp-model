DROP VIEW IF EXISTS sm_production_performance_kpi;

CREATE VIEW sm_production_performance_kpi AS
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
downtime AS (
    SELECT
        machine_id,
        site_id,
        date(start_time) AS kpi_date,
        SUM(downtime_minutes) AS total_downtime
    FROM fact_machine_downtime
    GROUP BY machine_id, site_id, date(start_time)
),
throughput AS (
    SELECT
        machine_id,
        site_id,
        date(timestamp) AS kpi_date,
        SUM(units_produced) AS units_produced,
        SUM(scrap_units) AS scrap_units,
        SUM(units_produced + scrap_units) AS total_units
    FROM fact_production_throughput
    GROUP BY machine_id, site_id, date(timestamp)
)
SELECT
    u.kpi_date,
    u.site_id,
    s.site_code,
    u.machine_id,
    m.machine_code,

    -- Runtime + Downtime
    u.runtime_minutes,
    COALESCE(d.total_downtime, u.downtime_minutes) AS downtime_minutes,
    (u.runtime_minutes + COALESCE(d.total_downtime, u.downtime_minutes)) AS total_minutes,

    -- Throughput
    t.units_produced,
    t.scrap_units,
    t.total_units,

    -- Scrap Rate
    CASE
        WHEN t.total_units = 0 THEN 0
        ELSE t.scrap_units * 1.0 / t.total_units
    END AS scrap_rate,

    -- OEE Components
    CASE
        WHEN (u.runtime_minutes + COALESCE(d.total_downtime, u.downtime_minutes)) = 0 THEN NULL
        ELSE u.runtime_minutes * 1.0 /
             (u.runtime_minutes + COALESCE(d.total_downtime, u.downtime_minutes))
    END AS availability,

    CASE
        WHEN u.runtime_minutes = 0 THEN NULL
        ELSE t.units_produced * 1.0 / u.runtime_minutes
    END AS performance,

    CASE
        WHEN t.total_units = 0 THEN NULL
        ELSE t.units_produced * 1.0 / t.total_units
    END AS quality,

    -- Full OEE
    CASE
        WHEN (u.runtime_minutes + COALESCE(d.total_downtime, u.downtime_minutes)) = 0
             OR u.runtime_minutes = 0
             OR t.total_units = 0
        THEN NULL
        ELSE
            (u.runtime_minutes * 1.0 /
             (u.runtime_minutes + COALESCE(d.total_downtime, u.downtime_minutes)))
            *
            (t.units_produced * 1.0 / u.runtime_minutes)
            *
            (t.units_produced * 1.0 / t.total_units)
    END AS oee

FROM usage u
JOIN dim_sites s ON u.site_id = s.site_id
JOIN dim_machines m ON u.machine_id = m.machine_id
LEFT JOIN downtime d
    ON u.machine_id = d.machine_id
   AND u.site_id = d.site_id
   AND u.kpi_date = d.kpi_date
LEFT JOIN throughput t
    ON u.machine_id = t.machine_id
   AND u.site_id = t.site_id
   AND u.kpi_date = t.kpi_date;
