
-- 1. Department-wise payroll cost
SELECT
    d.department_name,
    COUNT(DISTINCT p.employee_id) AS employee_count,
    ROUND(SUM(p.gross_pay), 2) AS total_gross_pay,
    ROUND(SUM(p.employer_cost), 2) AS total_employer_cost
FROM fact_payroll p
LEFT JOIN dim_department d
    ON p.department_id = d.department_id
GROUP BY d.department_name
ORDER BY total_employer_cost DESC;

-- 2. Monthly payroll trend
SELECT
    d.year,
    d.month_number,
    d.month_name,
    COUNT(DISTINCT p.employee_id) AS employee_count,
    ROUND(SUM(p.gross_pay), 2) AS total_gross_pay,
    ROUND(SUM(p.employer_cost), 2) AS total_employer_cost
FROM fact_payroll p
JOIN dim_date d ON p.date_key = d.date_key
GROUP BY d.year, d.month_number, d.month_name
ORDER BY d.year, d.month_number;

-- 3. Department-wise headcount and attrition
SELECT
    d.year,
    d.month_number,
    dept.department_name,
    h.headcount_start,
    h.hires,
    h.exits,
    h.voluntary_exits,
    h.headcount_end,
    h.attrition_rate_monthly_pct
FROM fact_headcount_monthly h
JOIN dim_date d ON h.date_key = d.date_key
JOIN dim_department dept ON h.department_id = dept.department_id
ORDER BY d.year, d.month_number, dept.department_name;

-- 4. Monthly attendance summary
SELECT
    d.year,
    d.month_number,
    d.month_name,
    COUNT(DISTINCT a.employee_id) AS employee_count,
    ROUND(SUM(a.scheduled_days), 2) AS scheduled_days,
    ROUND(SUM(a.present_days), 2) AS present_days,
    ROUND(AVG(a.attendance_rate), 2) AS avg_attendance_rate
FROM fact_attendance_monthly a
JOIN dim_date d ON a.date_key = d.date_key
GROUP BY d.year, d.month_number, d.month_name
ORDER BY d.year, d.month_number;
