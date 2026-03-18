-- ============================================================
-- Schemo - Government Scheme Aggregator Portal
-- Database Schema
-- ============================================================

CREATE DATABASE IF NOT EXISTS schemo_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE schemo_db;

-- ============================================================
-- Users Table
-- ============================================================
CREATE TABLE IF NOT EXISTS users (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(150)    NOT NULL,
    email       VARCHAR(200)    NOT NULL UNIQUE,
    phone_number VARCHAR(15)    NOT NULL UNIQUE,
    password    VARCHAR(255)    NOT NULL,
    age         INT             NOT NULL,
    gender      ENUM('Male','Female','Other') NOT NULL,
    community   ENUM('General','OBC','SC','ST','Minority','EWS') NOT NULL,
    occupation  ENUM('Student','Working Professional','Government Employee','Self Employed','Unemployed','Senior Citizen','Other') NOT NULL COMMENT 'User occupation / type',
    state       VARCHAR(100)    NOT NULL,
    created_at  TIMESTAMP       DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- Admins Table
-- ============================================================
CREATE TABLE IF NOT EXISTS admins (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    username    VARCHAR(100)    NOT NULL UNIQUE,
    password    VARCHAR(255)    NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Default admin: admin / admin123 (hashed at app startup)
-- The app.py seed_admin() function inserts this on first run.

-- ============================================================
-- Schemes Table
-- ============================================================
CREATE TABLE IF NOT EXISTS schemes (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    scheme_name         VARCHAR(255)    NOT NULL,
    description         TEXT            NOT NULL,
    eligibility         TEXT            NOT NULL,
    community           VARCHAR(255)    NOT NULL COMMENT 'Comma-separated communities or "All"',
    min_age             INT             DEFAULT 0,
    max_age             INT             DEFAULT 100,
    max_income          DECIMAL(12,2)   DEFAULT 999999999 COMMENT '0 means no income limit',
    benefits            TEXT            NOT NULL,
    documents_required  TEXT            NOT NULL,
    deadline            DATE            NULL,
    official_link       VARCHAR(500)    NOT NULL,
    created_at          TIMESTAMP       DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- Sample Scheme Data
-- ============================================================
INSERT INTO schemes (scheme_name, description, eligibility, community, min_age, max_age, max_income, benefits, documents_required, deadline, official_link) VALUES

('PM Kisan Samman Nidhi',
 'Financial support to farmer families with landholding up to 2 hectares. Provides direct income support to sustain farm-related expenses.',
 'Farmer families with cultivable land up to 2 hectares with age between 18 and 65. Annual household income below ₹1,50,000.',
 'All',
 18, 65, 150000,
 '₹6,000 per year in three equal installments of ₹2,000 each, directly credited to bank account.',
 'Aadhaar Card, Land ownership documents, Bank passbook, Mobile number',
 '2026-12-31',
 'https://pmkisan.gov.in'),

('PM Ujjwala Yojana',
 'To provide free LPG connections to women from below poverty line (BPL) households to replace unclean cooking fuels.',
 'Women aged 18 years or above from BPL families. Annual income below ₹1,20,000.',
 'All',
 18, 60, 120000,
 'Free LPG connection, one cylinder refill subsidy, EMI facility for stove and first refill.',
 'BPL Ration Card, Aadhaar Card, Bank account details, Passport-size photograph',
 '2027-03-31',
 'https://pmuy.gov.in'),

('Pradhan Mantri Awas Yojana (Urban)',
 'Housing for All mission providing affordable housing to economically weaker sections, low income groups and middle income groups in urban areas.',
 'EWS/LIG/MIG applicants with annual income up to ₹18 lakh. Applicant or family should not own a pucca house anywhere in India.',
 'EWS,General,OBC,SC,ST,Minority',
 21, 70, 1800000,
 'Interest subsidy of 3% to 6.5% on home loan, credit linked subsidy up to ₹2.67 lakh.',
 'Aadhaar Card, Income Certificate, Bank statements (6 months), Self-declaration of no house ownership',
 '2026-09-30',
 'https://pmaymis.gov.in'),

('National Scholarship Portal - Pre-Matric',
 'Scholarship for students belonging to SC/ST/OBC communities studying in Class 1 to 10 to encourage continuity in education.',
 'Students from SC/ST/OBC communities in Class 1–10. Family income below ₹2,50,000 per annum.',
 'SC,ST,OBC',
 5, 17, 250000,
 '₹1,000 to ₹3,500 per annum depending on class and day scholar/hostel status.',
 'School Enrollment Certificate, Caste Certificate, Income Certificate, Bank account of parent/guardian, Aadhaar Card',
 '2026-10-31',
 'https://scholarships.gov.in'),

('National Scholarship Portal - Post-Matric',
 'Scholarship for meritorious students from SC/ST/OBC/Minority communities studying Class 11 onwards to higher education.',
 'Students from SC/ST/OBC/Minority communities in Class 11 and above. Family annual income below ₹2,50,000.',
 'SC,ST,OBC,Minority',
 15, 30, 250000,
 'Maintenance allowance ₹300 to ₹1,200 per month and reimbursement of compulsory non-refundable fees.',
 'Marksheet of previous class, Caste Certificate, Income Certificate, College enrollment letter, Bank account, Aadhaar Card',
 '2026-11-30',
 'https://scholarships.gov.in'),

('Beti Bachao Beti Padhao',
 'Scheme to address declining Child Sex Ratio (CSR) and related issues of empowerment of women over a life cycle continuum.',
 'Girl child from birth to 18 years. Parents or guardians must be Indian citizens.',
 'All',
 0, 18, 999999999,
 'Conditional cash transfer, educational scholarship, awareness campaigns, skill training incentives.',
 'Birth certificate of girl child, Aadhaar Card of parents, Bank account of parents',
 '2027-03-31',
 'https://wcd.nic.in/bbbp-schemes'),

('Atal Pension Yojana',
 'Guaranteed minimum pension scheme for citizens in the unorganized sector providing pension of ₹1,000 to ₹5,000.',
 'Indian citizens aged 18 to 40, not a member of any other statutory social security scheme, having a savings bank account.',
 'All',
 18, 40, 999999999,
 'Guaranteed monthly pension of ₹1,000 to ₹5,000 after age 60. Nominee receives corpus amount on death.',
 'Aadhaar Card, Savings bank account, Mobile number linked to Aadhaar',
 NULL,
 'https://npscra.nsdl.co.in'),

('PM SVANidhi - Street Vendor Loan',
 'Micro-credit facility for street vendors to restart livelihoods affected by COVID-19 with enhanced credit limits on repayment.',
 'Street vendors engaged in vending in urban areas with a vending certificate or letter of recommendation. Age 18 to 60.',
 'All',
 18, 60, 360000,
 'Working capital loan of ₹10,000 (1st term), ₹20,000 (2nd term), ₹50,000 (3rd term). Interest subsidy of 7%.',
 'Vending Certificate / Letter of Recommendation, Aadhaar Card, Bank account details',
 '2026-12-31',
 'https://pmsvanidhi.mohua.gov.in'),

('EWS Scholarship for Higher Education',
 'Scholarship for economically weak section (EWS) students pursuing higher education in colleges and universities across India.',
 'Students belonging to EWS category with family income below ₹8 lakh per annum, enrolled in recognized institutions.',
 'EWS,General',
 17, 30, 800000,
 'Scholarship amount of ₹10,000 per year for graduate and post-graduate courses.',
 'EWS Certificate, Income Certificate, Aadhaar Card, College admission letter, Bank account',
 '2026-09-30',
 'https://scholarships.gov.in'),

('Stand-Up India Scheme',
 'Facilitates bank loans between ₹10 lakh to ₹1 crore to SC/ST and women borrowers for setting up greenfield enterprises.',
 'SC/ST borrowers or women entrepreneurs. New enterprise should be a greenfield project in manufacturing, services, or trading.',
 'SC,ST',
 18, 55, 999999999,
 'Bank loan from ₹10 lakh to ₹1 crore with repayment tenure of 7 years and moratorium of 18 months.',
 'Aadhaar Card, PAN Card, Business plan, Caste Certificate (for SC/ST), Bank account details, Proof of business address',
 '2027-03-31',
 'https://standupmitra.in'),

('PM Scholarship Scheme for Widows and Ex-Servicemen',
 'Scholarship for dependent wards and widows of ex-servicemen and ex-coast guard personnel for higher technical and professional education.',
 'Wards or widows of Ex-servicemen/Ex-coast guard. Minimum 60% marks in qualifying exam. Age below 26 years.',
 'All',
 18, 26, 999999999,
 '₹2,500 per month for boys and ₹3,000 per month for girls for approved courses.',
 'PPO of ex-serviceman, Aadhaar Card, Marksheets, Bonafide certificate, Bank account',
 '2026-10-31',
 'https://ksb.gov.in'),

('Minority Welfare Scholarship - Maulana Azad',
 'Merit-cum-means scholarship for students from minority communities to pursue professional and technical courses at undergrad and postgrad level.',
 'Students from minority communities (Muslim, Christian, Sikh, Buddhist, Jain, Zoroastrian). Family income below ₹2.5 lakh. Minimum 50% marks.',
 'Minority',
 17, 30, 250000,
 'Course fee reimbursement and maintenance allowance of ₹10,000 per year.',
 'Minority community certificate, Income Certificate, Aadhaar Card, Marksheets, Admission letter, Bank account',
 '2026-09-30',
 'https://maef.nic.in');

-- ============================================================
-- Migration: Replace income with occupation (run once on existing DBs)
-- ============================================================
-- If your database already exists with the `income` column, run these
-- two statements to migrate without losing existing data:
--
--   ALTER TABLE users
--       ADD COLUMN occupation
--           ENUM('Student','Working Professional','Government Employee',
--                'Self Employed','Unemployed','Senior Citizen','Other')
--           NOT NULL DEFAULT 'Other'
--           AFTER community;
--
--   ALTER TABLE users DROP COLUMN income;

-- Optional: Run this to update an existing users table
-- ALTER TABLE users ADD COLUMN phone_number VARCHAR(15) UNIQUE NOT NULL AFTER email;

-- ============================================================
