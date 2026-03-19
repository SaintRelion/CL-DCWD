/*
 Navicat Premium Dump SQL

 Source Server         : PostgreSQL 18
 Source Server Type    : PostgreSQL
 Source Server Version : 180001 (180001)
 Source Host           : localhost:5433
 Source Catalog        : dcwd_incidents
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 180001 (180001)
 File Encoding         : 65001

 Date: 18/03/2026 18:47:38
*/


-- ----------------------------
-- Sequence structure for incident_reports_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."incident_reports_id_seq";
CREATE SEQUENCE "public"."incident_reports_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for keywords_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."keywords_id_seq";
CREATE SEQUENCE "public"."keywords_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for locations_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."locations_id_seq";
CREATE SEQUENCE "public"."locations_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for posts_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."posts_id_seq";
CREATE SEQUENCE "public"."posts_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for users_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."users_id_seq";
CREATE SEQUENCE "public"."users_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Table structure for incident_reports
-- ----------------------------
DROP TABLE IF EXISTS "public"."incident_reports";
CREATE TABLE "public"."incident_reports" (
  "id" int4 NOT NULL DEFAULT nextval('incident_reports_id_seq'::regclass),
  "post_id" int4,
  "keyword_category_id" int4,
  "location_id" int4,
  "latitude" float8,
  "longitude" float8,
  "timestamp" timestamp(6) DEFAULT now(),
  "condition" varchar COLLATE "pg_catalog"."default",
  "status" varchar COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Records of incident_reports
-- ----------------------------
INSERT INTO "public"."incident_reports" VALUES (34, 42, 5, 3, 8.604, 123.3908, '2026-03-18 14:30:31.572172', 'None', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (35, 40, 5, 3, 8.604, 123.3908, '2026-03-18 14:31:49.812965', 'None', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (36, 39, 5, 7, 8.6205, 123.4023, '2026-03-18 14:33:53.252087', 'None', 'Pending');

-- ----------------------------
-- Table structure for keywords
-- ----------------------------
DROP TABLE IF EXISTS "public"."keywords";
CREATE TABLE "public"."keywords" (
  "id" int4 NOT NULL DEFAULT nextval('keywords_id_seq'::regclass),
  "word" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "language" varchar(20) COLLATE "pg_catalog"."default" NOT NULL,
  "category" varchar(50) COLLATE "pg_catalog"."default" NOT NULL
)
;

-- ----------------------------
-- Records of keywords
-- ----------------------------
INSERT INTO "public"."keywords" VALUES (1, 'walay tubig', 'Visayan', 'no_water');
INSERT INTO "public"."keywords" VALUES (2, 'tulo', 'Visayan', 'leak');
INSERT INTO "public"."keywords" VALUES (3, 'hugaw', 'Visayan', 'dirty_water');
INSERT INTO "public"."keywords" VALUES (4, 'no water', 'English', 'no_water');
INSERT INTO "public"."keywords" VALUES (5, 'leak', 'English', 'leak');
INSERT INTO "public"."keywords" VALUES (6, 'dirty', 'English', 'dirty_water');
INSERT INTO "public"."keywords" VALUES (7, 'walang tubig', 'Tagalog', 'no_water');
INSERT INTO "public"."keywords" VALUES (8, 'buslot', 'Tagalog', 'leak');
INSERT INTO "public"."keywords" VALUES (9, 'dumi', 'Tagalog', 'dirty_water');

-- ----------------------------
-- Table structure for locations
-- ----------------------------
DROP TABLE IF EXISTS "public"."locations";
CREATE TABLE "public"."locations" (
  "id" int4 NOT NULL DEFAULT nextval('locations_id_seq'::regclass),
  "barangay" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "street" varchar(150) COLLATE "pg_catalog"."default",
  "latitude" float8,
  "longitude" float8
)
;

-- ----------------------------
-- Records of locations
-- ----------------------------
INSERT INTO "public"."locations" VALUES (1, 'Antipolo', 'Riverside Road', 8.6021, 123.3921);
INSERT INTO "public"."locations" VALUES (2, 'Antipolo', 'Purok 1', 8.6032, 123.3915);
INSERT INTO "public"."locations" VALUES (3, 'Antipolo', 'Hilltop Drive', 8.604, 123.3908);
INSERT INTO "public"."locations" VALUES (4, 'Bagting', 'Market Road', 8.6142, 123.3987);
INSERT INTO "public"."locations" VALUES (5, 'Bagting', 'Purok Bagtingon', 8.6135, 123.3979);
INSERT INTO "public"."locations" VALUES (6, 'Bagting', 'Crossing Street', 8.6128, 123.3982);
INSERT INTO "public"."locations" VALUES (7, 'Banonong', 'Coastal Road', 8.6205, 123.4023);
INSERT INTO "public"."locations" VALUES (8, 'Banonong', 'San Jose Street', 8.6198, 123.4019);
INSERT INTO "public"."locations" VALUES (9, 'Banonong', 'Purok Matahum', 8.6209, 123.403);
INSERT INTO "public"."locations" VALUES (10, 'Baylimango', 'Central Road', 8.6074, 123.3865);
INSERT INTO "public"."locations" VALUES (11, 'Baylimango', 'Purok Bayli', 8.6079, 123.3859);
INSERT INTO "public"."locations" VALUES (12, 'Baylimango', 'Mango Street', 8.6085, 123.3862);
INSERT INTO "public"."locations" VALUES (13, 'Burgos', 'Burgos Proper Road', 8.6183, 123.4081);
INSERT INTO "public"."locations" VALUES (14, 'Burgos', 'Purok 2', 8.6179, 123.4075);
INSERT INTO "public"."locations" VALUES (15, 'Burgos', 'Hillview Street', 8.6187, 123.4089);
INSERT INTO "public"."locations" VALUES (19, 'Dawo', 'Dawo Proper Road', 8.5985, 123.3889);
INSERT INTO "public"."locations" VALUES (20, 'Dawo', 'Purok Farmers', 8.5992, 123.3893);
INSERT INTO "public"."locations" VALUES (21, 'Dawo', 'Highway Road', 8.5979, 123.3878);
INSERT INTO "public"."locations" VALUES (22, 'Ilaya', 'Ilaya Main Road', 8.6265, 123.413);
INSERT INTO "public"."locations" VALUES (23, 'Ilaya', 'Purok Ilayon', 8.6259, 123.4124);
INSERT INTO "public"."locations" VALUES (24, 'Ilaya', 'Upper Crossing', 8.6269, 123.4135);
INSERT INTO "public"."locations" VALUES (25, 'Larayan', 'Larayan Road', 8.615, 123.405);
INSERT INTO "public"."locations" VALUES (26, 'Larayan', 'Purok 5', 8.6156, 123.4056);
INSERT INTO "public"."locations" VALUES (27, 'Larayan', 'Forest Drive', 8.616, 123.4062);
INSERT INTO "public"."locations" VALUES (28, 'Linabo', 'Linabo Proper', 8.6122, 123.3995);
INSERT INTO "public"."locations" VALUES (29, 'Linabo', 'Purok Linabohan', 8.6117, 123.3999);
INSERT INTO "public"."locations" VALUES (30, 'Linabo', 'Spring Road', 8.6128, 123.3988);
INSERT INTO "public"."locations" VALUES (31, 'Liyang', 'Liyang Street', 8.6008, 123.3933);
INSERT INTO "public"."locations" VALUES (32, 'Liyang', 'Purok Malipayon', 8.6012, 123.3928);
INSERT INTO "public"."locations" VALUES (33, 'Liyang', 'Station Road', 8.6017, 123.3939);
INSERT INTO "public"."locations" VALUES (34, 'Maria Cristina', 'Cristina Road', 8.6177, 123.4045);
INSERT INTO "public"."locations" VALUES (35, 'Maria Cristina', 'Purok Cristinahan', 8.6171, 123.4049);
INSERT INTO "public"."locations" VALUES (36, 'Maria Cristina', 'Sunrise Lane', 8.6182, 123.4052);
INSERT INTO "public"."locations" VALUES (37, 'Napo', 'Napo Street', 8.5948, 123.3825);
INSERT INTO "public"."locations" VALUES (38, 'Napo', 'Purok Napohan', 8.5942, 123.3829);
INSERT INTO "public"."locations" VALUES (39, 'Napo', 'Baybay Road', 8.5938, 123.3834);
INSERT INTO "public"."locations" VALUES (40, 'Owaon', 'Owaon Proper Road', 8.6299, 123.4168);
INSERT INTO "public"."locations" VALUES (41, 'Owaon', 'Purok 3', 8.6292, 123.4163);
INSERT INTO "public"."locations" VALUES (42, 'Owaon', 'Hillside Drive', 8.6304, 123.4172);
INSERT INTO "public"."locations" VALUES (43, 'Polo', 'Fisherman Road', 8.6015, 123.3957);
INSERT INTO "public"."locations" VALUES (44, 'Polo', 'Purok Polohan', 8.6022, 123.3951);
INSERT INTO "public"."locations" VALUES (45, 'Polo', 'Coastline Street', 8.6019, 123.3963);
INSERT INTO "public"."locations" VALUES (46, 'Potol', 'Potol Street', 8.6096, 123.3907);
INSERT INTO "public"."locations" VALUES (47, 'Potol', 'Purok 4', 8.6091, 123.3901);
INSERT INTO "public"."locations" VALUES (48, 'Potol', 'Old Road', 8.61, 123.3913);
INSERT INTO "public"."locations" VALUES (49, 'San Pedro', 'San Pedro Main Road', 8.6208, 123.4077);
INSERT INTO "public"."locations" VALUES (50, 'San Pedro', 'Purok Sanramon', 8.6212, 123.4071);
INSERT INTO "public"."locations" VALUES (51, 'San Pedro', 'Crossway Road', 8.6202, 123.4082);
INSERT INTO "public"."locations" VALUES (52, 'San Vicente', 'San Vicente Road', 8.5969, 123.3862);
INSERT INTO "public"."locations" VALUES (53, 'San Vicente', 'Purok Vicente', 8.5963, 123.3858);
INSERT INTO "public"."locations" VALUES (54, 'San Vicente', 'Valley Road', 8.5973, 123.3869);
INSERT INTO "public"."locations" VALUES (55, 'Sinonoc', 'Sinonoc Street', 8.6283, 123.4152);
INSERT INTO "public"."locations" VALUES (56, 'Sinonoc', 'Purok Sinonokan', 8.6277, 123.4146);
INSERT INTO "public"."locations" VALUES (57, 'Sinonoc', 'Hillside Road', 8.6289, 123.4158);
INSERT INTO "public"."locations" VALUES (58, 'Sta. Cruz', 'Cruz Proper Road', 8.6133, 123.4022);
INSERT INTO "public"."locations" VALUES (59, 'Sta. Cruz', 'Purok Cruzana', 8.6128, 123.4016);
INSERT INTO "public"."locations" VALUES (60, 'Sta. Cruz', 'Old Church Road', 8.614, 123.4028);
INSERT INTO "public"."locations" VALUES (61, 'Sulangon', 'Sulangon Main Road', 8.6062, 123.3898);
INSERT INTO "public"."locations" VALUES (62, 'Sulangon', 'Purok Sulanganon', 8.6057, 123.3892);
INSERT INTO "public"."locations" VALUES (63, 'Sulangon', 'Farmers Lane', 8.6068, 123.3903);
INSERT INTO "public"."locations" VALUES (64, 'Talisay', 'Talisay Street', 8.5949, 123.3839);
INSERT INTO "public"."locations" VALUES (65, 'Talisay', 'Purok Talisayon', 8.5944, 123.3833);
INSERT INTO "public"."locations" VALUES (66, 'Talisay', 'Beach Road', 8.5955, 123.3844);
INSERT INTO "public"."locations" VALUES (67, 'Tamion', 'Tamion Road', 8.6247, 123.4119);
INSERT INTO "public"."locations" VALUES (68, 'Tamion', 'Purok Tamionon', 8.6242, 123.4113);
INSERT INTO "public"."locations" VALUES (69, 'Tamion', 'Northside Lane', 8.6252, 123.4125);
INSERT INTO "public"."locations" VALUES (70, 'Upper Sicayab', 'Sicayab Upper Road', 8.6222, 123.4099);
INSERT INTO "public"."locations" VALUES (71, 'Upper Sicayab', 'Purok Upperon', 8.6217, 123.4093);
INSERT INTO "public"."locations" VALUES (72, 'Upper Sicayab', 'Hillside Drive', 8.6228, 123.4105);
INSERT INTO "public"."locations" VALUES (17, 'Cawa Cawa', 'Purok Gawaon', 8.623, 123.4101);
INSERT INTO "public"."locations" VALUES (18, 'Cawa Cawa', 'Riverbank Street', 8.624, 123.4108);
INSERT INTO "public"."locations" VALUES (16, 'Cawa Cawa', 'Cawa Cawa', 8.6235, 123.4106);

-- ----------------------------
-- Table structure for posts
-- ----------------------------
DROP TABLE IF EXISTS "public"."posts";
CREATE TABLE "public"."posts" (
  "id" int4 NOT NULL DEFAULT nextval('posts_id_seq'::regclass),
  "raw_post_text" text COLLATE "pg_catalog"."default" NOT NULL,
  "nlp_intent" varchar(255) COLLATE "pg_catalog"."default",
  "date_scraped" timestamp(6) DEFAULT now(),
  "status" varchar(255) COLLATE "pg_catalog"."default",
  "location_id" int4,
  "latitude" float8,
  "longitude" float8
)
;

-- ----------------------------
-- Records of posts
-- ----------------------------
INSERT INTO "public"."posts" VALUES (36, 'uiiiiiiiiiiiiiiiiiiiiiiiiiiiiijklhhl', '7', '2026-01-14 04:01:22.372301', 'Under Evaluation', 1, NULL, NULL);
INSERT INTO "public"."posts" VALUES (37, 'aetsdfg', 'Unknown', '2026-01-14 04:01:22.417037', 'Under Evaluation', 2, NULL, NULL);
INSERT INTO "public"."posts" VALUES (34, 'nag leak diari sa antipolo riverside, gahapon pa dyud ni', '5', '2026-01-14 04:01:22.263448', 'Under Evaluation', 3, NULL, NULL);
INSERT INTO "public"."posts" VALUES (35, 'naa napoy hugaw ang tubig diri sa dawo', '3', '2026-01-14 04:01:22.317419', 'Under Evaluation', 6, NULL, NULL);
INSERT INTO "public"."posts" VALUES (38, 'helloasdf', '2', '2026-01-14 04:01:22.458787', 'Non-Incident', 7, NULL, NULL);
INSERT INTO "public"."posts" VALUES (42, 'hello', '2', '2026-03-11 15:45:03.695072', 'Actual Incident', NULL, NULL, NULL);
INSERT INTO "public"."posts" VALUES (40, 'hugaw ang tubig daari sa bagting tungod sa market road', '3', '2026-03-11 02:17:59.474346', 'Actual Incident', 9, NULL, NULL);
INSERT INTO "public"."posts" VALUES (39, 'mga sir, sa hillview street diari burgos kay hugaw kaayo ang tubig, kinsa may nag labay gud diri og balas', '3', '2026-01-14 04:12:34.678153', 'Actual Incident', 8, NULL, NULL);

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS "public"."users";
CREATE TABLE "public"."users" (
  "id" int4 NOT NULL DEFAULT nextval('users_id_seq'::regclass),
  "username" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "password" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "role" varchar(20) COLLATE "pg_catalog"."default" NOT NULL,
  "created_at" timestamp(6) DEFAULT CURRENT_TIMESTAMP,
  "email" varchar COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO "public"."users" VALUES (1, 'operator', '123', 'operator', '2026-03-11 01:54:52.783825', NULL);
INSERT INTO "public"."users" VALUES (2, 'tubero', '123', 'tubero', '2026-03-11 05:29:25.151745', 'pyromaniac33143@gmail.com');

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."incident_reports_id_seq"
OWNED BY "public"."incident_reports"."id";
SELECT setval('"public"."incident_reports_id_seq"', 3069, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."keywords_id_seq"
OWNED BY "public"."keywords"."id";
SELECT setval('"public"."keywords_id_seq"', 9, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."locations_id_seq"
OWNED BY "public"."locations"."id";
SELECT setval('"public"."locations_id_seq"', 72, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."posts_id_seq"
OWNED BY "public"."posts"."id";
SELECT setval('"public"."posts_id_seq"', 42, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."users_id_seq"
OWNED BY "public"."users"."id";
SELECT setval('"public"."users_id_seq"', 3, true);

-- ----------------------------
-- Primary Key structure for table incident_reports
-- ----------------------------
ALTER TABLE "public"."incident_reports" ADD CONSTRAINT "incident_reports_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table keywords
-- ----------------------------
ALTER TABLE "public"."keywords" ADD CONSTRAINT "keywords_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table locations
-- ----------------------------
ALTER TABLE "public"."locations" ADD CONSTRAINT "locations_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table posts
-- ----------------------------
ALTER TABLE "public"."posts" ADD CONSTRAINT "posts_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Uniques structure for table users
-- ----------------------------
ALTER TABLE "public"."users" ADD CONSTRAINT "users_username_key" UNIQUE ("username");

-- ----------------------------
-- Checks structure for table users
-- ----------------------------
ALTER TABLE "public"."users" ADD CONSTRAINT "users_role_check" CHECK (role::text = ANY (ARRAY['operator'::character varying, 'tubero'::character varying, 'manager'::character varying]::text[]));

-- ----------------------------
-- Primary Key structure for table users
-- ----------------------------
ALTER TABLE "public"."users" ADD CONSTRAINT "users_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Foreign Keys structure for table incident_reports
-- ----------------------------
ALTER TABLE "public"."incident_reports" ADD CONSTRAINT "incident_reports_keyword_category_id_fkey" FOREIGN KEY ("keyword_category_id") REFERENCES "public"."keywords" ("id") ON DELETE SET NULL ON UPDATE NO ACTION;
ALTER TABLE "public"."incident_reports" ADD CONSTRAINT "incident_reports_location_id_fkey" FOREIGN KEY ("location_id") REFERENCES "public"."locations" ("id") ON DELETE SET NULL ON UPDATE NO ACTION;
