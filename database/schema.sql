-- ============================================================
-- Schemo - Government Scheme Aggregator Portal
-- PostgreSQL / Supabase Schema
-- Run this in: Supabase Dashboard → SQL Editor
-- ============================================================

-- ============================================================
-- Users Table
-- ============================================================
CREATE TABLE IF NOT EXISTS users (
    id           BIGSERIAL PRIMARY KEY,
    name         VARCHAR(150)  NOT NULL,
    email        VARCHAR(200)  NOT NULL UNIQUE,
    phone_number VARCHAR(15)   NOT NULL UNIQUE,
    password     VARCHAR(255)  NOT NULL,
    age          INT           NOT NULL,
    gender       VARCHAR(10)   NOT NULL CHECK (gender IN ('Male','Female','Other')),
    community    VARCHAR(20)   NOT NULL CHECK (community IN ('General','OBC','SC','ST','Minority','EWS')),
    occupation   VARCHAR(60)   NOT NULL CHECK (occupation IN ('Student','Working Professional','Government Employee','Self Employed','Unemployed','Senior Citizen','Other')),
    state        VARCHAR(100)  NOT NULL,
    created_at   TIMESTAMPTZ   DEFAULT NOW()
);

-- ============================================================
-- Admins Table
-- ============================================================
CREATE TABLE IF NOT EXISTS admins (
    id         BIGSERIAL PRIMARY KEY,
    username   VARCHAR(100) NOT NULL UNIQUE,
    password   VARCHAR(255) NOT NULL
);
-- Default admin (admin / admin123) is seeded by app.py on first run.

-- ============================================================
-- Schemes Table
-- ============================================================
CREATE TABLE IF NOT EXISTS schemes (
    id                  BIGSERIAL PRIMARY KEY,
    scheme_name         VARCHAR(255)   NOT NULL,
    description         TEXT           NOT NULL,
    eligibility         TEXT           NOT NULL,
    community           VARCHAR(255)   NOT NULL,  -- comma-separated or 'All'
    min_age             INT            DEFAULT 0,
    max_age             INT            DEFAULT 100,
    max_income          NUMERIC(12,2)  DEFAULT 999999999,  -- 0 = no income limit
    benefits            TEXT           NOT NULL,
    documents_required  TEXT           NOT NULL,
    deadline            DATE           NULL,
    official_link       VARCHAR(500)   NOT NULL,
    created_at          TIMESTAMPTZ    DEFAULT NOW()
);

-- ============================================================
-- Row Level Security (RLS)
-- Run AFTER creating tables. Uses Supabase service role key
-- from the backend, so RLS is bypassed server-side.
-- ============================================================
ALTER TABLE users   ENABLE ROW LEVEL SECURITY;
ALTER TABLE admins  ENABLE ROW LEVEL SECURITY;
ALTER TABLE schemes ENABLE ROW LEVEL SECURITY;

-- Allow service role full access (backend uses service role key)
CREATE POLICY "service_role_all_users"   ON users   FOR ALL USING (true);
CREATE POLICY "service_role_all_admins"  ON admins  FOR ALL USING (true);
CREATE POLICY "service_role_all_schemes" ON schemes FOR ALL USING (true);

-- ============================================================
-- Sample Scheme Data
-- ============================================================
INSERT INTO schemes (scheme_name, description, eligibility, community, min_age, max_age, max_income, benefits, documents_required, deadline, official_link) VALUES

('PM Kisan Samman Nidhi',
 'Financial support to farmer families with landholding up to 2 hectares.',
 'Farmer families with cultivable land up to 2 hectares. Annual household income below 1,50,000.',
 'All', 18, 65, 150000,
 '6000 per year in three installments of 2000 each, directly credited to bank account.',
 'Aadhaar Card, Land ownership documents, Bank passbook, Mobile number',
 '2026-12-31', 'https://pmkisan.gov.in'),

('PM Ujjwala Yojana',
 'Free LPG connections to women from below poverty line households.',
 'Women aged 18 or above from BPL families. Annual income below 1,20,000.',
 'All', 18, 60, 120000,
 'Free LPG connection, one cylinder refill subsidy, EMI facility for stove and first refill.',
 'BPL Ration Card, Aadhaar Card, Bank account details, Passport-size photograph',
 '2027-03-31', 'https://pmuy.gov.in'),

('Pradhan Mantri Awas Yojana (Urban)',
 'Affordable housing for EWS/LIG/MIG applicants in urban areas.',
 'EWS/LIG/MIG applicants with annual income up to 18 lakh. No pucca house anywhere in India.',
 'EWS,General,OBC,SC,ST,Minority', 21, 70, 1800000,
 'Interest subsidy of 3% to 6.5% on home loan, credit linked subsidy up to 2.67 lakh.',
 'Aadhaar Card, Income Certificate, Bank statements (6 months), Self-declaration of no house ownership',
 '2026-09-30', 'https://pmaymis.gov.in'),

('National Scholarship Portal - Pre-Matric',
 'Scholarship for SC/ST/OBC students in Class 1 to 10.',
 'Students from SC/ST/OBC communities in Class 1-10. Family income below 2,50,000 per annum.',
 'SC,ST,OBC', 5, 17, 250000,
 '1000 to 3500 per annum depending on class and day scholar/hostel status.',
 'School Enrollment Certificate, Caste Certificate, Income Certificate, Bank account, Aadhaar Card',
 '2026-10-31', 'https://scholarships.gov.in'),

('National Scholarship Portal - Post-Matric',
 'Scholarship for SC/ST/OBC/Minority students in Class 11 and above.',
 'Students from SC/ST/OBC/Minority communities in Class 11 and above. Family income below 2,50,000.',
 'SC,ST,OBC,Minority', 15, 30, 250000,
 'Maintenance allowance 300 to 1200 per month and reimbursement of compulsory fees.',
 'Marksheet, Caste Certificate, Income Certificate, College enrollment letter, Bank account, Aadhaar Card',
 '2026-11-30', 'https://scholarships.gov.in'),

('Beti Bachao Beti Padhao',
 'Scheme to address declining Child Sex Ratio and empower women.',
 'Girl child from birth to 18 years. Parents or guardians must be Indian citizens.',
 'All', 0, 18, 999999999,
 'Conditional cash transfer, educational scholarship, skill training incentives.',
 'Birth certificate of girl child, Aadhaar Card of parents, Bank account of parents',
 '2027-03-31', 'https://wcd.nic.in/bbbp-schemes'),

('Atal Pension Yojana',
 'Guaranteed minimum pension scheme for citizens in the unorganized sector.',
 'Indian citizens aged 18 to 40, not a member of any statutory social security scheme.',
 'All', 18, 40, 999999999,
 'Guaranteed monthly pension of 1000 to 5000 after age 60.',
 'Aadhaar Card, Savings bank account, Mobile number linked to Aadhaar',
 NULL, 'https://npscra.nsdl.co.in'),

('PM SVANidhi - Street Vendor Loan',
 'Micro-credit facility for street vendors to restart livelihoods.',
 'Street vendors in urban areas with a vending certificate. Age 18 to 60.',
 'All', 18, 60, 360000,
 'Working capital loan of 10000 (1st), 20000 (2nd), 50000 (3rd term). Interest subsidy 7%.',
 'Vending Certificate, Aadhaar Card, Bank account details',
 '2026-12-31', 'https://pmsvanidhi.mohua.gov.in'),

('EWS Scholarship for Higher Education',
 'Scholarship for EWS students pursuing higher education.',
 'EWS students with family income below 8 lakh, enrolled in recognized institutions.',
 'EWS,General', 17, 30, 800000,
 'Scholarship amount of 10000 per year for graduate and post-graduate courses.',
 'EWS Certificate, Income Certificate, Aadhaar Card, College admission letter, Bank account',
 '2026-09-30', 'https://scholarships.gov.in'),

('Stand-Up India Scheme',
 'Bank loans for SC/ST and women borrowers for greenfield enterprises.',
 'SC/ST borrowers or women entrepreneurs setting up a new greenfield enterprise.',
 'SC,ST', 18, 55, 999999999,
 'Bank loan from 10 lakh to 1 crore, repayment tenure 7 years, moratorium 18 months.',
 'Aadhaar Card, PAN Card, Business plan, Caste Certificate, Bank account, Business address proof',
 '2027-03-31', 'https://standupmitra.in'),

('PM Scholarship Scheme for Widows and Ex-Servicemen',
 'Scholarship for wards and widows of ex-servicemen for higher technical education.',
 'Wards or widows of Ex-servicemen. Minimum 60% marks in qualifying exam. Age below 26.',
 'All', 18, 26, 999999999,
 '2500 per month for boys and 3000 per month for girls for approved courses.',
 'PPO of ex-serviceman, Aadhaar Card, Marksheets, Bonafide certificate, Bank account',
 '2026-10-31', 'https://ksb.gov.in'),

('Minority Welfare Scholarship - Maulana Azad',
 'Merit-cum-means scholarship for minority community students in professional courses.',
 'Students from minority communities. Family income below 2.5 lakh. Minimum 50% marks.',
 'Minority', 17, 30, 250000,
 'Course fee reimbursement and maintenance allowance of 10000 per year.',
 'Minority community certificate, Income Certificate, Aadhaar Card, Marksheets, Admission letter, Bank account',
 '2026-09-30', 'https://maef.nic.in');
