
-- 1. Attendance: check whether employee/month is unique
SELECT
    employee_id,
    DATE_TRUNC('month', period_end_date)::date AS payroll_month,
    COUNT(*) AS row_count
FROM fact_attendance_monthly
GROUP BY employee_id, DATE_TRUNC('month', period_end_date)::date
HAVING COUNT(*) > 1
ORDER BY payroll_month, employee_id;


-- 2. Payroll: check employee/month duplicates
SELECT
    employee_id,
    DATE_TRUNC('month', period_end_date)::date AS payroll_month,
    COUNT(*) AS row_count,
    SUM(gross_pay) AS total_gross_pay
FROM fact_payroll
GROUP BY employee_id, DATE_TRUNC('month', period_end_date)::date
HAVING COUNT(*) > 1
ORDER BY payroll_month, employee_id;


-- 3. Leave: check whether leave request ID is unique
SELECT
    leave_request_id,
    COUNT(*) AS row_count
FROM fact_leave
GROUP BY leave_request_id
HAVING COUNT(*) > 1;


-- 4. Headcount: check department/month uniqueness
SELECT
    department_id,
    DATE_TRUNC('month', month_start_date)::date AS month,
    COUNT(*) AS row_count
FROM fact_headcount_monthly
GROUP BY department_id, DATE_TRUNC('month', month_start_date)::date
HAVING COUNT(*) > 1;
