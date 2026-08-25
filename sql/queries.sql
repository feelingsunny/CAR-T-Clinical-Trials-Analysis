-- ============================================================
-- CAR-T Clinical Trials Analysis Queries
-- Database: cart_trials
-- Author: Yang Liu
-- ============================================================


-- Query 1: CAR-T Trial Growth by Year
-- Shows annual trend of new trials and total patients enrolled
SELECT 
    start_year,
    COUNT(*) AS new_trials,
    SUM(enrollment) AS total_patients
FROM trials
WHERE start_year IS NOT NULL
GROUP BY start_year
ORDER BY start_year;


-- Query 2: Trial Count and Enrollment by Cancer Type
-- Identifies which cancer types have the most CAR-T research activity
SELECT 
    c.condition,
    COUNT(DISTINCT t.trial_id) AS trial_count,
    ROUND(AVG(t.enrollment), 0) AS avg_enrollment,
    SUM(CASE WHEN t.status = 'COMPLETED' THEN 1 ELSE 0 END) AS completed
FROM trials t
JOIN conditions c ON t.trial_id = c.trial_id
GROUP BY c.condition
ORDER BY trial_count DESC;


-- Query 3: Trial Completion Rate by Phase
-- Compares completion and termination rates across trial phases
SELECT 
    phase,
    COUNT(*) AS total,
    SUM(CASE WHEN status = 'COMPLETED' THEN 1 ELSE 0 END) AS completed,
    SUM(CASE WHEN status = 'TERMINATED' THEN 1 ELSE 0 END) AS terminated,
    ROUND(100.0 * SUM(CASE WHEN status = 'COMPLETED' 
          THEN 1 ELSE 0 END) / COUNT(*), 1) AS completion_rate_pct
FROM trials
WHERE phase IS NOT NULL
GROUP BY phase
ORDER BY phase;


-- Query 4: Geographic Distribution (US vs China vs Global)
-- Highlights US and China dominance in CAR-T research
SELECT 
    l.country,
    COUNT(DISTINCT t.trial_id) AS trial_count,
    ROUND(AVG(t.enrollment), 0) AS avg_enrollment,
    SUM(CASE WHEN t.status = 'COMPLETED' THEN 1 ELSE 0 END) AS completed
FROM trials t
JOIN locations l ON t.trial_id = l.trial_id
GROUP BY l.country
ORDER BY trial_count DESC;


-- Query 5: CAR-T Product Analysis
-- Compares leading CAR-T products by trial volume and enrollment
SELECT 
    i.intervention_name,
    COUNT(DISTINCT t.trial_id) AS trial_count,
    ROUND(AVG(t.enrollment), 0) AS avg_enrollment,
    SUM(CASE WHEN t.status = 'COMPLETED' THEN 1 ELSE 0 END) AS completed
FROM trials t
JOIN interventions i ON t.trial_id = i.trial_id
GROUP BY i.intervention_name
ORDER BY trial_count DESC;


-- Query 6: Pediatric vs Adult Trials by Phase (Window Function)
-- Uses window function to compare pediatric vs adult trial distribution
SELECT 
    phase,
    is_pediatric,
    COUNT(*) AS trial_count,
    ROUND(AVG(enrollment), 0) AS avg_enrollment,
    ROUND(AVG(COUNT(*)) OVER (PARTITION BY phase), 1) AS avg_trials_per_phase
FROM trials
GROUP BY phase, is_pediatric
ORDER BY phase, is_pediatric;