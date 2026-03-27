-- ============================================================
-- Schemo - Government Scheme Aggregator Portal
-- PostgreSQL / Supabase Schema
-- Run this FULLY in: Supabase Dashboard → SQL Editor → New Query
-- ============================================================

-- Drop existing tables if re-running (safe re-run)
DROP TABLE IF EXISTS schemes  CASCADE;
DROP TABLE IF EXISTS users    CASCADE;
DROP TABLE IF EXISTS admins   CASCADE;

-- ============================================================
-- 1. USERS TABLE
-- ============================================================
CREATE TABLE users (
    id           BIGSERIAL PRIMARY KEY,
    name         VARCHAR(150)  NOT NULL,
    email        VARCHAR(200)  NOT NULL UNIQUE,
    phone_number VARCHAR(20)   NOT NULL UNIQUE,
    password     VARCHAR(255)  NOT NULL,
    age          INT           NOT NULL DEFAULT 0,
    gender       VARCHAR(20)   NOT NULL DEFAULT 'Other',
    community    VARCHAR(50)   NOT NULL DEFAULT 'General',
    occupation   VARCHAR(100)  NOT NULL DEFAULT 'Other',
    state        VARCHAR(100)  NOT NULL DEFAULT 'Not Specified',
    created_at   TIMESTAMPTZ   DEFAULT NOW()
);

-- ============================================================
-- 2. ADMINS TABLE
-- ============================================================
CREATE TABLE admins (
    id         BIGSERIAL PRIMARY KEY,
    username   VARCHAR(100) NOT NULL UNIQUE,
    password   VARCHAR(255) NOT NULL
);

-- ============================================================
-- 3. SCHEMES TABLE
-- ============================================================
CREATE TABLE schemes (
    id                  BIGSERIAL PRIMARY KEY,
    scheme_name         VARCHAR(255)   NOT NULL,
    description         TEXT           NOT NULL DEFAULT '',
    eligibility         TEXT           NOT NULL DEFAULT '',
    community           VARCHAR(255)   NOT NULL DEFAULT 'All',
    min_age             INT            DEFAULT 0,
    max_age             INT            DEFAULT 100,
    max_income          NUMERIC(15,2)  DEFAULT 0,
    benefits            TEXT           NOT NULL DEFAULT '',
    documents_required  TEXT           NOT NULL DEFAULT '',
    deadline            DATE           NULL,
    official_link       VARCHAR(500)   NOT NULL DEFAULT '',
    created_at          TIMESTAMPTZ    DEFAULT NOW()
);

-- ============================================================
-- 4. ROW LEVEL SECURITY
-- ============================================================
ALTER TABLE users   ENABLE ROW LEVEL SECURITY;
ALTER TABLE admins  ENABLE ROW LEVEL SECURITY;
ALTER TABLE schemes ENABLE ROW LEVEL SECURITY;

-- Allow ALL operations via service role key (used by backend)
CREATE POLICY "allow_all_users"   ON users   FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "allow_all_admins"  ON admins  FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "allow_all_schemes" ON schemes FOR ALL TO service_role USING (true) WITH CHECK (true);

-- Also allow anon read on schemes (for public browse page)
CREATE POLICY "anon_read_schemes" ON schemes FOR SELECT TO anon USING (true);

-- ============================================================
-- 5. SAMPLE SCHEMES DATA
-- ============================================================
INSERT INTO schemes (scheme_name, description, eligibility, community, min_age, max_age, max_income, benefits, documents_required, deadline, official_link) VALUES

('PM Kisan Samman Nidhi',
 'Financial support to farmer families providing direct income support of Rs.6000 per year.',
 'Small and marginal farmers with cultivable land. Must be registered in PM Kisan portal.',
 'All', 18, 70, 0,
 'Rs.6000 per year in 3 installments of Rs.2000 directly to bank account.',
 'Aadhaar Card|Land Records (Khatoni)|Bank Passbook|Mobile Number',
 NULL, 'https://pmkisan.gov.in'),

('PM Ujjwala Yojana',
 'Free LPG gas connection scheme for women from BPL households.',
 'Women above 18 years from BPL families without existing LPG connection.',
 'All', 18, 60, 120000,
 'Free LPG gas connection + first refill free + stove free of cost.',
 'Aadhaar Card|BPL Ration Card|Bank Account|Passport Photo',
 NULL, 'https://pmujjwalayojana.com'),

('Ayushman Bharat PMJAY',
 'Health insurance scheme providing coverage up to Rs.5 lakh per family per year.',
 'Families listed in SECC 2011 database or state scheme beneficiaries.',
 'All', 0, 100, 0,
 'Health insurance up to Rs.5 lakh per family per year. Cashless treatment at 25000+ hospitals.',
 'Aadhaar Card|Ration Card|PMJAY Eligibility Letter',
 NULL, 'https://pmjay.gov.in'),

('National Scholarship Portal - Post Matric',
 'Scholarship for SC/ST/OBC/Minority students in Class 11 and above.',
 'Students from SC/ST/OBC/Minority communities in Class 11 and above. Family income below Rs.2.5 lakh.',
 'SC,ST,OBC,Minority', 15, 30, 250000,
 'Maintenance allowance Rs.300 to Rs.1200 per month + full tuition fee reimbursement.',
 'Marksheet|Caste Certificate|Income Certificate|College Enrollment Letter|Bank Account|Aadhaar Card',
 '2026-11-30', 'https://scholarships.gov.in'),

('PM Awas Yojana Gramin',
 'Free housing scheme for BPL families in rural areas without pucca house.',
 'BPL families in rural areas without pucca house listed in SECC 2011.',
 'All', 18, 65, 0,
 'Rs.1.20 lakh in plain areas and Rs.1.30 lakh in hilly areas for house construction.',
 'Aadhaar Card|BPL Card|Land Documents|Bank Account',
 NULL, 'https://pmayg.nic.in'),

('Beti Bachao Beti Padhao',
 'Scheme to promote welfare and education of girl children across India.',
 'Girl children from 0 to 18 years. Parents must be Indian citizens.',
 'All', 0, 18, 0,
 'Education support, welfare programs and awareness campaigns for girl child.',
 'Birth Certificate|Aadhaar Card of Parent|Bank Account of Parent',
 NULL, 'https://wcd.nic.in'),

('Sukanya Samriddhi Yojana',
 'High-interest savings scheme for girl child education and marriage expenses.',
 'Parents or guardians of girl child below 10 years.',
 'All', 0, 10, 0,
 '8.2% interest per annum tax-free savings. Maturity on girl turning 21.',
 'Birth Certificate of Girl Child|Aadhaar Card of Parent|Bank Account',
 NULL, 'https://nsiindia.gov.in'),

('Atal Pension Yojana',
 'Guaranteed pension scheme for unorganized sector workers.',
 'Indian citizens between 18 to 40 years with bank account, not covered under any statutory social security.',
 'All', 18, 40, 0,
 'Guaranteed monthly pension of Rs.1000 to Rs.5000 after age 60.',
 'Aadhaar Card|Bank Account|Mobile Number',
 NULL, 'https://npscra.nsdl.co.in'),

('PM Mudra Yojana',
 'Micro loan scheme for small businesses and entrepreneurs without collateral.',
 'Small business owners and entrepreneurs. No collateral required.',
 'All', 18, 65, 0,
 'Loans up to Rs.10 lakh: Shishu (up to Rs.50K), Kishore (Rs.50K-5L), Tarun (Rs.5L-10L).',
 'Aadhaar Card|Business Proof|Bank Account|Passport Photo',
 NULL, 'https://mudra.org.in'),

('PM Kaushal Vikas Yojana',
 'Free skill training scheme for youth with certification and cash reward.',
 'Youth between 15 to 45 years seeking skill development and employment.',
 'All', 15, 45, 0,
 'Free skill training + Rs.8000 reward on successful certification.',
 'Aadhaar Card|Bank Account|Educational Certificate',
 NULL, 'https://pmkvyofficial.org'),

('MGNREGS - 100 Days Employment',
 '100 days guaranteed employment scheme for rural households.',
 'Any adult member of rural household willing to do unskilled manual work.',
 'All', 18, 60, 0,
 '100 days guaranteed employment per year at Rs.220 to Rs.350 per day.',
 'Aadhaar Card|Job Card from Gram Panchayat|Bank Account',
 NULL, 'https://nrega.nic.in'),

('Standup India',
 'Bank loans for SC/ST and women entrepreneurs for greenfield enterprises.',
 'SC/ST borrowers or women entrepreneurs setting up a new greenfield enterprise.',
 'SC,ST', 18, 65, 0,
 'Loans from Rs.10 lakh to Rs.1 crore for new business setup.',
 'Aadhaar Card|PAN Card|Business Plan|Caste Certificate|Bank Account',
 NULL, 'https://standupmitra.in'),

('Indira Gandhi National Old Age Pension',
 'Monthly pension for elderly BPL citizens above 60 years.',
 'BPL citizens above 60 years.',
 'All', 60, 100, 0,
 'Rs.200 per month for age 60-79 and Rs.500 per month for age 80 and above.',
 'Aadhaar Card|Age Proof|BPL Certificate|Bank Account',
 NULL, 'https://nsap.nic.in'),

('Kalaignar Magalir Urimai Thittam',
 'Monthly cash transfer scheme for women in Tamil Nadu.',
 'Women above 21 years who are head of family with annual income below Rs.2.5 lakh in Tamil Nadu.',
 'All', 21, 60, 250000,
 'Rs.1000 per month direct cash transfer to bank account.',
 'Aadhaar Card|Ration Card|Bank Account|Income Certificate',
 NULL, 'https://tn.gov.in'),

('Pudhumai Penn Scheme',
 'Monthly stipend for girl students from Tamil Nadu government schools in higher education.',
 'Girls who studied Class 6 to 12 in Tamil Nadu government schools now in higher education.',
 'All', 18, 30, 0,
 'Rs.1000 per month stipend until graduation.',
 'School Transfer Certificate|College Admission Proof|Aadhaar Card|Bank Account',
 NULL, 'https://tn.gov.in'),

('Post Matric Scholarship SC Students',
 'Scholarship for Scheduled Caste students in Class 11 and above.',
 'SC students in Class 11 and above with family income below Rs.2.5 lakh.',
 'SC', 15, 35, 250000,
 'Full tuition fee reimbursement + maintenance allowance Rs.230 to Rs.1200 per month.',
 'Aadhaar Card|Caste Certificate|Income Certificate|Bank Account|Marksheet',
 '2026-11-30', 'https://scholarships.gov.in'),

('PM Jan Dhan Yojana',
 'Financial inclusion scheme providing zero-balance bank accounts to unbanked citizens.',
 'All Indian citizens without a bank account.',
 'All', 10, 100, 0,
 'Zero balance bank account + RuPay debit card + Rs.2 lakh accident insurance + Rs.30000 life cover.',
 'Aadhaar Card|Passport Photo',
 NULL, 'https://pmjdy.gov.in'),

('PM Fasal Bima Yojana',
 'Crop insurance scheme providing financial support to farmers for crop loss.',
 'All farmers growing notified crops in notified areas.',
 'All', 18, 70, 0,
 'Full insurance coverage for crop loss at 2% premium for Kharif and 1.5% for Rabi crops.',
 'Aadhaar Card|Land Record|Bank Account|Sowing Certificate',
 NULL, 'https://pmfby.gov.in'),

('Janani Suraksha Yojana',
 'Cash incentive for institutional delivery for pregnant women from BPL families.',
 'Pregnant women from BPL families delivering in government or accredited hospitals.',
 'All', 18, 45, 0,
 'Cash incentive of Rs.1400 in rural areas and Rs.1000 in urban areas.',
 'Aadhaar Card|BPL Card|Bank Account|MCP Card',
 NULL, 'https://nhm.gov.in'),

('PM SVANidhi Street Vendor Loan',
 'Working capital loan for street vendors to restart livelihoods.',
 'Street vendors in urban areas with vending certificate. Age 18 to 60.',
 'All', 18, 60, 0,
 'Loan Rs.10000 (1st), Rs.20000 (2nd), Rs.50000 (3rd). Interest subsidy 7%.',
 'Vending Certificate|Aadhaar Card|Bank Account',
 NULL, 'https://pmsvanidhi.mohua.gov.in');
