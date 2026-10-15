
-- PulseIQ Analytics Warehouse Schema
-- Database: PostgreSQL
-- 10 business tables

-- 1. Department dimension
CREATE TABLE IF NOT EXISTS dim_department (
    department_id VARCHAR(20) PRIMARY KEY,
    department_name VARCHAR(150) NOT NULL,
    cost_center VARCHAR(30),
    description TEXT,
    is_leadership VARCHAR(5)
);

-- 2. Location dimension
CREATE TABLE IF NOT EXISTS dim_location (
    work_location VARCHAR(100) PRIMARY KEY
);

-- 3. Role dimension
CREATE TABLE IF NOT EXISTS dim_role (
    role_id VARCHAR(20) PRIMARY KEY,
    department_id VARCHAR(20),
    role_title VARCHAR(150),
    level INTEGER,
    grade VARCHAR(50),
    band_min_annual NUMERIC(14,2),
    band_mid_annual NUMERIC(14,2),
    band_max_annual NUMERIC(14,2),
    overtime_eligible VARCHAR(5),
    band_reference_year INTEGER
);

-- 4. Date dimension
CREATE TABLE IF NOT EXISTS dim_date (
    date_key INTEGER PRIMARY KEY,
    date DATE NOT NULL UNIQUE,
    year INTEGER,
    quarter INTEGER,
    month_number INTEGER,
    month_name VARCHAR(20),
    year_month VARCHAR(10),
    week_of_year INTEGER,
    day_of_week VARCHAR(15),
    is_weekend VARCHAR(5),
    is_holiday VARCHAR(5),
    is_working_day VARCHAR(5),
    financial_year VARCHAR(15),
    fiscal_quarter VARCHAR(10),
    fiscal_month_number INTEGER,
    is_month_end VARCHAR(5),
    month_start_date DATE,
    month_end_date DATE
);

-- 5. Leave type dimension
CREATE TABLE IF NOT EXISTS dim_leave_type (
    leave_type_code VARCHAR(10) PRIMARY KEY,
    leave_type_name VARCHAR(100) NOT NULL,
    pay_type VARCHAR(30),
    annual_quota_days NUMERIC(8,2),
    prorated_for_joiners VARCHAR(5),
    carry_forward_allowed VARCHAR(5),
    max_carry_forward_days NUMERIC(8,2),
    policy_note TEXT
);

-- 6. Employee dimension with history (SCD Type 2)
CREATE TABLE IF NOT EXISTS dim_employee (
    employee_key INTEGER PRIMARY KEY,
    employee_id VARCHAR(30) NOT NULL,
    full_name VARCHAR(150),
    gender VARCHAR(20),
    date_of_birth DATE,
    hire_date DATE,
    exit_date DATE,
    employment_status VARCHAR(30),
    employment_type VARCHAR(30),
    department_id VARCHAR(20),
    role_id VARCHAR(20),
    role_title VARCHAR(150),
    job_level INTEGER,
    manager_id VARCHAR(30),
    work_location VARCHAR(100),
    work_mode VARCHAR(30),
    highest_education VARCHAR(150),
    valid_from DATE NOT NULL,
    valid_to DATE,
    is_current VARCHAR(5),
    change_reason VARCHAR(100),
    UNIQUE (employee_id, valid_from),
    CONSTRAINT fk_employee_location
        FOREIGN KEY (work_location)
        REFERENCES dim_location(work_location)
);

-- 7. Monthly attendance fact
-- Grain: one row per employee per month
CREATE TABLE IF NOT EXISTS fact_attendance_monthly (
    attendance_fact_id VARCHAR(30) PRIMARY KEY,
    employee_id VARCHAR(30),
    date_key INTEGER,
    employee_key INTEGER,
    department_id VARCHAR(20),
    scheduled_days NUMERIC(8,2),
    present_days NUMERIC(8,2),
    wfh_days NUMERIC(8,2),
    half_days_unpaid NUMERIC(8,2),
    paid_leave_days NUMERIC(8,2),
    unpaid_absence_days NUMERIC(8,2),
    late_arrivals INTEGER,
    avg_hours_worked NUMERIC(8,2),
    overtime_hours NUMERIC(8,2),
    attendance_rate NUMERIC(8,4),
    period_end_date DATE
);

-- 8. Payroll fact
-- Grain: one row per payroll item
CREATE TABLE IF NOT EXISTS fact_payroll (
    payroll_item_id VARCHAR(30) PRIMARY KEY,
    run_id VARCHAR(30),
    employee_id VARCHAR(30),
    date_key INTEGER,
    employee_key INTEGER,
    period_end_date DATE,
    department_id VARCHAR(20),
    role_id VARCHAR(20),
    payable_days NUMERIC(8,2),
    lop_days NUMERIC(8,2),
    overtime_hours_paid NUMERIC(8,2),
    variable_pay_type VARCHAR(100),
    monthly_fixed_gross NUMERIC(16,2),
    basic NUMERIC(16,2),
    hra NUMERIC(16,2),
    conveyance NUMERIC(16,2),
    medical NUMERIC(16,2),
    special_allowance NUMERIC(16,2),
    earned_fixed_pay NUMERIC(16,2),
    overtime_pay NUMERIC(16,2),
    variable_pay NUMERIC(16,2),
    gross_pay NUMERIC(16,2),
    pf_employee NUMERIC(16,2),
    esi_employee NUMERIC(16,2),
    professional_tax NUMERIC(16,2),
    tds NUMERIC(16,2),
    other_deductions NUMERIC(16,2),
    total_deductions NUMERIC(16,2),
    net_pay NUMERIC(16,2),
    pf_employer NUMERIC(16,2),
    esi_employer NUMERIC(16,2),
    employer_cost NUMERIC(16,2),
    headcount_flag INTEGER
);

-- 9. Leave fact
-- Grain: one row per leave request
CREATE TABLE IF NOT EXISTS fact_leave (
    leave_request_id VARCHAR(30) PRIMARY KEY,
    employee_id VARCHAR(30),
    employee_key INTEGER,
    leave_type_code VARCHAR(10),
    start_date_key INTEGER,
    end_date_key INTEGER,
    start_date DATE,
    end_date DATE,
    days NUMERIC(8,2),
    status VARCHAR(30),
    applied_on DATE,
    decided_on DATE,
    approver_id VARCHAR(30),
    reason TEXT
);

-- 10. Monthly headcount fact
-- Grain: one row per department per month
CREATE TABLE IF NOT EXISTS fact_headcount_monthly (
    date_key INTEGER,
    month_start_date DATE,
    department_id VARCHAR(20),
    headcount_start INTEGER,
    hires INTEGER,
    exits INTEGER,
    voluntary_exits INTEGER,
    transfers_in INTEGER,
    transfers_out INTEGER,
    headcount_end INTEGER,
    attrition_rate_monthly_pct NUMERIC(10,4),
    PRIMARY KEY (date_key, department_id)
);

-- Indexes for commonly used joins and filters

CREATE INDEX IF NOT EXISTS idx_employee_id
    ON dim_employee(employee_id);

CREATE INDEX IF NOT EXISTS idx_employee_department
    ON dim_employee(department_id);

CREATE INDEX IF NOT EXISTS idx_employee_role
    ON dim_employee(role_id);

CREATE INDEX IF NOT EXISTS idx_attendance_date
    ON fact_attendance_monthly(date_key);

CREATE INDEX IF NOT EXISTS idx_attendance_employee
    ON fact_attendance_monthly(employee_key);

CREATE INDEX IF NOT EXISTS idx_payroll_date
    ON fact_payroll(date_key);

CREATE INDEX IF NOT EXISTS idx_payroll_department
    ON fact_payroll(department_id);

CREATE INDEX IF NOT EXISTS idx_leave_employee
    ON fact_leave(employee_key);

CREATE INDEX IF NOT EXISTS idx_headcount_department
    ON fact_headcount_monthly(department_id);
