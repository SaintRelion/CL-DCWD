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

 Date: 07/05/2026 06:28:15
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
  "timestamp" timestamp(6) DEFAULT now(),
  "status" varchar COLLATE "pg_catalog"."default",
  "street_name" varchar(255) COLLATE "pg_catalog"."default",
  "remarks" text COLLATE "pg_catalog"."default",
  "plumber_name" varchar(255) COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Records of incident_reports
-- ----------------------------
INSERT INTO "public"."incident_reports" VALUES (1, 6, 3, 4, '2026-04-03 13:26:27.561803', 'Closed', '', '', 'tubero');
INSERT INTO "public"."incident_reports" VALUES (2, 8, 2, 7, '2026-03-11 18:00:27.561803', 'Active', '', '', 'tubero');
INSERT INTO "public"."incident_reports" VALUES (3, 12, 1, 70, '2026-04-27 20:05:27.561803', 'Closed', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (4, 20, 1, 55, '2026-03-24 07:14:27.561803', 'Closed', '', '', 'tubero');
INSERT INTO "public"."incident_reports" VALUES (5, 22, 2, 46, '2026-03-18 22:49:27.561803', 'Active', '', '', 'tubero');
INSERT INTO "public"."incident_reports" VALUES (6, 22, 3, 70, '2026-03-27 09:16:27.561803', 'Active', '', '', 'tubero');
INSERT INTO "public"."incident_reports" VALUES (7, 26, 3, 43, '2026-03-28 19:56:27.561803', 'Closed', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (8, 31, 3, 31, '2026-03-07 15:42:27.561803', 'Closed', '', '', 'tubero');
INSERT INTO "public"."incident_reports" VALUES (9, 40, 2, 37, '2026-03-05 14:31:27.561803', 'Closed', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (10, 34, 1, 34, '2026-04-24 13:07:27.561803', 'Closed', '', '', 'tubero');
INSERT INTO "public"."incident_reports" VALUES (11, 20, 2, 40, '2026-05-02 00:29:27.561803', 'Closed', '', '', 'tubero');
INSERT INTO "public"."incident_reports" VALUES (12, 40, 1, 34, '2026-04-06 19:36:27.561803', 'Active', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (13, 44, 1, 22, '2026-02-27 14:16:27.561803', 'Closed', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (14, 45, 3, 64, '2026-02-06 11:12:27.561803', 'Active', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (15, 53, 1, 70, '2026-03-08 04:46:27.561803', 'Closed', '', '', 'tubero');
INSERT INTO "public"."incident_reports" VALUES (16, 20, 3, 17, '2026-02-17 19:41:27.561803', 'Closed', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (17, 62, 2, 67, '2026-03-27 02:52:27.561803', 'Closed', '', '', 'tubero');
INSERT INTO "public"."incident_reports" VALUES (18, 58, 1, 64, '2026-04-09 02:51:27.561803', 'Closed', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (19, 63, 2, 61, '2026-02-23 02:04:27.561803', 'Active', '', '', 'tubero');
INSERT INTO "public"."incident_reports" VALUES (20, 67, 3, 49, '2026-02-13 19:45:27.561803', 'Active', '', '', 'tubero');
INSERT INTO "public"."incident_reports" VALUES (21, 68, 1, 1, '2026-03-02 10:30:27.561803', 'Active', '', '', 'tubero');
INSERT INTO "public"."incident_reports" VALUES (22, 74, 3, 7, '2026-04-11 17:46:27.561803', 'Closed', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (23, 72, 2, 43, '2026-04-11 10:55:27.561803', 'Closed', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (24, 78, 3, 17, '2026-04-26 23:46:27.561803', 'Active', '', '', 'tubero');
INSERT INTO "public"."incident_reports" VALUES (25, 83, 2, 4, '2026-02-09 08:47:27.561803', 'Closed', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (26, 10, 3, 22, '2026-03-30 04:34:27.561803', 'Active', '', '', 'tubero');
INSERT INTO "public"."incident_reports" VALUES (27, 86, 3, 19, '2026-03-23 01:41:27.561803', 'Closed', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (28, 95, 2, 13, '2026-02-12 09:48:27.561803', 'Closed', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (29, 94, 1, 55, '2026-04-06 00:26:27.561803', 'Closed', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (30, 40, 3, 46, '2026-03-24 04:00:27.561803', 'Closed', '', '', 'tubero');
INSERT INTO "public"."incident_reports" VALUES (31, 101, 2, 17, '2026-02-27 21:34:27.561803', 'Closed', '', '', 'tubero');
INSERT INTO "public"."incident_reports" VALUES (32, 103, 3, 46, '2026-03-20 13:25:27.561803', 'Closed', '', '', 'tubero');
INSERT INTO "public"."incident_reports" VALUES (33, 50, 3, 70, '2026-03-03 01:07:27.561803', 'Closed', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (34, 110, 3, 46, '2026-03-31 01:38:27.561803', 'Closed', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (35, 110, 1, 52, '2026-04-27 23:23:27.561803', 'Active', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (36, 30, 2, 13, '2026-05-04 15:27:27.561803', 'Closed', '', '', 'tubero');
INSERT INTO "public"."incident_reports" VALUES (37, 120, 1, 19, '2026-02-10 19:37:27.561803', 'Closed', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (38, 121, 2, 46, '2026-02-19 16:33:27.561803', 'Active', '', '', 'tubero');
INSERT INTO "public"."incident_reports" VALUES (39, 127, 2, 55, '2026-04-22 15:21:27.561803', 'Closed', '', '', 'tubero');
INSERT INTO "public"."incident_reports" VALUES (40, 40, 1, 34, '2026-04-03 03:52:27.561803', 'Closed', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (41, 130, 1, 46, '2026-05-05 23:51:27.561803', 'Closed', '', '', 'tubero');
INSERT INTO "public"."incident_reports" VALUES (42, 137, 3, 25, '2026-02-16 11:38:27.561803', 'Active', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (43, 137, 2, 13, '2026-03-12 04:19:27.561803', 'Closed', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (44, 140, 3, 64, '2026-04-22 18:16:27.561803', 'Active', '', '', 'tubero');
INSERT INTO "public"."incident_reports" VALUES (45, 141, 2, 37, '2026-02-25 04:27:27.561803', 'Closed', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (46, 143, 2, 4, '2026-02-27 20:20:27.561803', 'Closed', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (47, 151, 3, 25, '2026-04-29 14:15:27.561803', 'Active', '', '', 'tubero');
INSERT INTO "public"."incident_reports" VALUES (48, 150, 3, 13, '2026-02-09 13:07:27.561803', 'Closed', '', '', 'tubero');
INSERT INTO "public"."incident_reports" VALUES (49, 150, 2, 43, '2026-03-02 21:42:27.561803', 'Closed', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (50, 10, 3, 64, '2026-03-02 09:08:27.561803', 'Closed', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (51, 50, 2, 67, '2026-05-06 01:56:27.561803', 'Closed', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (52, 158, 2, 40, '2026-02-13 02:33:27.561803', 'Closed', '', '', 'tubero');
INSERT INTO "public"."incident_reports" VALUES (53, 170, 2, 13, '2026-02-07 21:52:27.561803', 'Closed', '', '', 'tubero');
INSERT INTO "public"."incident_reports" VALUES (54, 165, 2, 17, '2026-03-23 06:00:27.561803', 'Closed', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (55, 172, 2, 61, '2026-03-11 10:03:27.561803', 'Active', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (56, 10, 2, 58, '2026-04-16 12:52:27.561803', 'Active', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (57, 175, 1, 28, '2026-05-05 19:00:27.561803', 'Closed', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (58, 50, 2, 31, '2026-03-09 06:27:27.561803', 'Closed', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (59, 184, 2, 67, '2026-04-18 10:49:27.561803', 'Closed', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (60, 191, 3, 28, '2026-02-21 12:13:27.561803', 'Closed', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (61, 188, 1, 1, '2026-03-05 02:35:27.561803', 'Closed', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (62, 194, 3, 37, '2026-02-25 04:39:27.561803', 'Closed', '', '', 'tubero');
INSERT INTO "public"."incident_reports" VALUES (63, 194, 3, 25, '2026-04-14 01:52:27.561803', 'Active', '', '', 'tubero');
INSERT INTO "public"."incident_reports" VALUES (64, 199, 1, 25, '2026-03-18 04:56:27.561803', 'Active', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (65, 198, 2, 52, '2026-02-09 15:46:27.561803', 'Closed', '', '', 'tubero');
INSERT INTO "public"."incident_reports" VALUES (66, 50, 1, 34, '2026-02-12 09:19:27.561803', 'Closed', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (67, 212, 3, 40, '2026-03-19 21:35:27.561803', 'Closed', '', '', 'tubero');
INSERT INTO "public"."incident_reports" VALUES (68, 30, 2, 10, '2026-02-19 04:13:27.561803', 'Closed', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (69, 30, 3, 13, '2026-02-13 13:49:27.561803', 'Closed', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (70, 212, 3, 49, '2026-03-20 21:57:27.561803', 'Closed', '', '', 'tubero');
INSERT INTO "public"."incident_reports" VALUES (71, 218, 1, 46, '2026-02-13 20:24:27.561803', 'Active', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (72, 226, 1, 28, '2026-03-19 13:21:27.561803', 'Active', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (73, 230, 2, 13, '2026-02-25 15:28:27.561803', 'Active', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (74, 40, 3, 37, '2026-03-12 11:17:27.561803', 'Closed', '', '', 'tubero');
INSERT INTO "public"."incident_reports" VALUES (75, 227, 2, 70, '2026-02-14 11:14:27.561803', 'Closed', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (76, 233, 2, 61, '2026-04-04 01:23:27.561803', 'Closed', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (77, 234, 1, 46, '2026-04-25 06:41:27.561803', 'Active', '', '', 'tubero');
INSERT INTO "public"."incident_reports" VALUES (78, 241, 3, 4, '2026-04-25 14:10:27.561803', 'Closed', '', '', 'tubero');
INSERT INTO "public"."incident_reports" VALUES (79, 20, 1, 10, '2026-02-13 23:26:27.561803', 'Active', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (80, 243, 1, 31, '2026-04-22 13:24:27.561803', 'Closed', '', '', 'tubero');
INSERT INTO "public"."incident_reports" VALUES (81, 249, 2, 1, '2026-04-06 14:40:27.561803', 'Closed', '', '', 'tubero');
INSERT INTO "public"."incident_reports" VALUES (82, 255, 2, 10, '2026-03-16 05:55:27.561803', 'Active', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (83, 30, 1, 17, '2026-02-16 02:12:27.561803', 'Active', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (84, 263, 1, 25, '2026-04-04 05:23:27.561803', 'Active', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (85, 258, 3, 49, '2026-03-22 16:28:27.561803', 'Active', '', '', 'tubero');
INSERT INTO "public"."incident_reports" VALUES (86, 40, 1, 10, '2026-05-06 17:24:27.561803', 'Closed', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (87, 269, 3, 17, '2026-04-25 08:12:27.561803', 'Active', '', '', 'tubero');
INSERT INTO "public"."incident_reports" VALUES (88, 275, 3, 61, '2026-02-20 05:07:27.561803', 'Closed', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (89, 273, 2, 55, '2026-03-25 12:55:27.561803', 'Closed', '', '', 'tubero');
INSERT INTO "public"."incident_reports" VALUES (90, 276, 1, 34, '2026-02-26 07:55:27.561803', 'Closed', '', '', 'tubero');
INSERT INTO "public"."incident_reports" VALUES (91, 30, 1, 37, '2026-04-24 01:06:27.561803', 'Closed', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (92, 286, 2, 61, '2026-04-20 07:05:27.561803', 'Closed', '', '', 'tubero');
INSERT INTO "public"."incident_reports" VALUES (93, 40, 2, 52, '2026-03-09 21:33:27.561803', 'Closed', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (94, 284, 1, 19, '2026-03-10 08:47:27.561803', 'Active', '', '', 'tubero');
INSERT INTO "public"."incident_reports" VALUES (95, 292, 3, 10, '2026-02-25 20:58:27.561803', 'Active', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (96, 293, 3, 4, '2026-03-06 12:23:27.561803', 'Active', '', '', 'tubero');
INSERT INTO "public"."incident_reports" VALUES (97, 301, 2, 70, '2026-04-09 01:46:27.561803', 'Active', '', '', 'tubero');
INSERT INTO "public"."incident_reports" VALUES (98, 30, 1, 49, '2026-02-19 14:56:27.561803', 'Active', '', '', 'mark');
INSERT INTO "public"."incident_reports" VALUES (99, 299, 2, 70, '2026-03-18 15:27:27.561803', 'Closed', '', '', 'tubero');
INSERT INTO "public"."incident_reports" VALUES (100, 311, 3, 61, '2026-04-07 15:44:27.561803', 'Active', '', '', 'mark');

-- ----------------------------
-- Table structure for keywords
-- ----------------------------
DROP TABLE IF EXISTS "public"."keywords";
CREATE TABLE "public"."keywords" (
  "id" int4 NOT NULL DEFAULT nextval('keywords_id_seq'::regclass),
  "category" varchar(50) COLLATE "pg_catalog"."default" NOT NULL
)
;

-- ----------------------------
-- Records of keywords
-- ----------------------------
INSERT INTO "public"."keywords" VALUES (1, 'no_water');
INSERT INTO "public"."keywords" VALUES (2, 'leak');
INSERT INTO "public"."keywords" VALUES (3, 'dirty_water');

-- ----------------------------
-- Table structure for locations
-- ----------------------------
DROP TABLE IF EXISTS "public"."locations";
CREATE TABLE "public"."locations" (
  "id" int4 NOT NULL DEFAULT nextval('locations_id_seq'::regclass),
  "barangay" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "latitude" float8,
  "longitude" float8
)
;

-- ----------------------------
-- Records of locations
-- ----------------------------
INSERT INTO "public"."locations" VALUES (1, 'Antipolo', 8.6021, 123.3921);
INSERT INTO "public"."locations" VALUES (4, 'Bagting', 8.6142, 123.3987);
INSERT INTO "public"."locations" VALUES (7, 'Banonong', 8.6205, 123.4023);
INSERT INTO "public"."locations" VALUES (10, 'Baylimango', 8.6074, 123.3865);
INSERT INTO "public"."locations" VALUES (13, 'Burgos', 8.6183, 123.4081);
INSERT INTO "public"."locations" VALUES (19, 'Dawo', 8.5985, 123.3889);
INSERT INTO "public"."locations" VALUES (22, 'Ilaya', 8.6265, 123.413);
INSERT INTO "public"."locations" VALUES (25, 'Larayan', 8.615, 123.405);
INSERT INTO "public"."locations" VALUES (28, 'Linabo', 8.6122, 123.3995);
INSERT INTO "public"."locations" VALUES (31, 'Liyang', 8.6008, 123.3933);
INSERT INTO "public"."locations" VALUES (34, 'Maria Cristina', 8.6177, 123.4045);
INSERT INTO "public"."locations" VALUES (37, 'Napo', 8.5948, 123.3825);
INSERT INTO "public"."locations" VALUES (40, 'Owaon', 8.6299, 123.4168);
INSERT INTO "public"."locations" VALUES (43, 'Polo', 8.6015, 123.3957);
INSERT INTO "public"."locations" VALUES (46, 'Potol', 8.6096, 123.3907);
INSERT INTO "public"."locations" VALUES (49, 'San Pedro', 8.6208, 123.4077);
INSERT INTO "public"."locations" VALUES (52, 'San Vicente', 8.5969, 123.3862);
INSERT INTO "public"."locations" VALUES (55, 'Sinonoc', 8.6283, 123.4152);
INSERT INTO "public"."locations" VALUES (58, 'Sta. Cruz', 8.6133, 123.4022);
INSERT INTO "public"."locations" VALUES (61, 'Sulangon', 8.6062, 123.3898);
INSERT INTO "public"."locations" VALUES (64, 'Talisay', 8.5949, 123.3839);
INSERT INTO "public"."locations" VALUES (67, 'Tamion', 8.6247, 123.4119);
INSERT INTO "public"."locations" VALUES (70, 'Upper Sicayab', 8.6222, 123.4099);
INSERT INTO "public"."locations" VALUES (17, 'Cawa Cawa', 8.623, 123.4101);

-- ----------------------------
-- Table structure for posts
-- ----------------------------
DROP TABLE IF EXISTS "public"."posts";
CREATE TABLE "public"."posts" (
  "id" int4 NOT NULL DEFAULT nextval('posts_id_seq'::regclass),
  "raw_post_text" text COLLATE "pg_catalog"."default" NOT NULL,
  "date_scraped" timestamp(6) DEFAULT now(),
  "status" varchar(255) COLLATE "pg_catalog"."default",
  "location_id" int4,
  "latitude" float8,
  "longitude" float8,
  "nlp_intent" varchar(255) COLLATE "pg_catalog"."default",
  "scraper_init" timestamp(6),
  "username" varchar(255) COLLATE "pg_catalog"."default",
  "profile_link" varchar(255) COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Records of posts
-- ----------------------------
INSERT INTO "public"."posts" VALUES (333, 'Wai agas sa Sinonoc, sinonoc street', '2026-05-07 01:13:18.294588', 'under evaluation', 55, 8.6283, 123.4152, 'no_water', '2026-05-07 01:13:18.61106', 'Mark Joseph Macxilum Ligoro', 'https://www.facebook.com/profile.php?id=100033355176794');
INSERT INTO "public"."posts" VALUES (334, 'Lubog ang tubig sa tamion, tamion road', '2026-05-07 01:16:40.924433', 'under evaluation', 67, 8.6247, 123.4119, 'dirty_water', '2026-05-07 01:13:18.61106', 'Mark Joseph Macxilum Ligoro', 'https://www.facebook.com/profile.php?id=100033355176794');
INSERT INTO "public"."posts" VALUES (335, 'haynako bakit walang tubig dito sa bagting market road', '2026-05-07 01:16:40.932006', 'under evaluation', 4, 8.6142, 123.3987, 'no_water', '2026-05-07 01:13:18.61106', 'Mark Joseph Macxilum Ligoro', 'https://www.facebook.com/profile.php?id=100033355176794');
INSERT INTO "public"."posts" VALUES (336, 'ga leak daari sa bagting market road plss ayha ni ninyo', '2026-05-07 01:16:40.94236', 'under evaluation', 4, 8.6142, 123.3987, 'leak', '2026-05-07 01:13:18.61106', 'Mark Joseph Macxilum Ligoro', 'https://www.facebook.com/profile.php?id=100033355176794');
INSERT INTO "public"."posts" VALUES (337, 'unsa maning nga lubog mn KAAYO ang tubig daari sa burgos purok 2', '2026-05-07 01:16:40.95391', 'under evaluation', 13, 8.6183, 123.4081, 'dirty_water', '2026-05-07 01:13:18.61106', 'Mark Joseph Macxilum Ligoro', 'https://www.facebook.com/profile.php?id=100033355176794');
INSERT INTO "public"."posts" VALUES (338, 'diri sa Ilaya main road, naay hugaw ang tubig, Kinsa man goy ga labay2 ani diri', '2026-05-07 01:16:40.959806', 'under evaluation', 22, 8.6265, 123.413, 'dirty_water', '2026-05-07 01:13:18.61106', 'Mark Joseph Macxilum Ligoro', 'https://www.facebook.com/profile.php?id=100033355176794');
INSERT INTO "public"."posts" VALUES (339, 'ga tulo ang tubig daari sa Antipolo purok 1', '2026-05-07 01:16:40.963524', 'under evaluation', 1, 8.6021, 123.3921, 'leak', '2026-05-07 01:13:18.61106', 'Mark Joseph Macxilum Ligoro', 'https://www.facebook.com/profile.php?id=100033355176794');
INSERT INTO "public"."posts" VALUES (340, 'hugaw ang tubig diri sa bagting costal road', '2026-05-07 01:16:40.967562', 'under evaluation', 4, 8.6142, 123.3987, 'dirty_water', '2026-05-07 01:13:18.61106', 'Mark Joseph Macxilum Ligoro', 'https://www.facebook.com/profile.php?id=100033355176794');
INSERT INTO "public"."posts" VALUES (341, 'hugaw ang tubig sa bagting market road', '2026-05-07 01:16:40.971305', 'under evaluation', 4, 8.6142, 123.3987, 'dirty_water', '2026-05-07 01:13:18.61106', 'Mark Joseph Macxilum Ligoro', 'https://www.facebook.com/profile.php?id=100033355176794');
INSERT INTO "public"."posts" VALUES (342, 'hugaw tubig bagting area', '2026-05-07 01:16:40.973937', 'under evaluation', 4, 8.6142, 123.3987, 'dirty_water', '2026-05-07 01:13:18.61106', 'Mark Joseph Macxilum Ligoro', 'https://www.facebook.com/profile.php?id=100033355176794');
INSERT INTO "public"."posts" VALUES (343, 'walay agas ang tubig daari sa talisay tamoin road', '2026-05-07 01:16:40.978607', 'under evaluation', 64, 8.5949, 123.3839, 'no_water', '2026-05-07 01:13:18.61106', 'Mark Joseph Macxilum Ligoro', 'https://www.facebook.com/profile.php?id=100033355176794');
INSERT INTO "public"."posts" VALUES (344, 'naunsa maning tubig daari sa sulangon sa purok cruzana hugaw mn kaayo', '2026-05-07 01:16:40.984242', 'under evaluation', 61, 8.6062, 123.3898, 'dirty_water', '2026-05-07 01:13:18.61106', 'Mark Joseph Macxilum Ligoro', 'https://www.facebook.com/profile.php?id=100033355176794');
INSERT INTO "public"."posts" VALUES (345, 'walai tubig sa Ilaya,purok rose', '2026-05-07 01:16:40.986563', 'under evaluation', NULL, NULL, NULL, 'no_water', '2026-05-07 01:13:18.61106', 'Nhoj New', 'https://www.facebook.com/profile.php?id=61574717976299');
INSERT INTO "public"."posts" VALUES (346, 'asa dapit ang office sa DCWD?', '2026-05-07 01:16:40.988954', 'non-incident', NULL, NULL, NULL, 'Unknown', '2026-05-07 01:13:18.61106', 'Mark Joseph Macxilum Ligoro', 'https://www.facebook.com/profile.php?id=100033355176794');
INSERT INTO "public"."posts" VALUES (347, 'sa tamoin ang dumi Ng tubig dito purok tamoinon', '2026-05-07 01:16:40.991456', 'under evaluation', 67, 8.6247, 123.4119, 'dirty_water', '2026-05-07 01:13:18.61106', 'Mark Joseph Macxilum Ligoro', 'https://www.facebook.com/profile.php?id=100033355176794');
INSERT INTO "public"."posts" VALUES (348, 'leak ang tubig daari sa Antipolo purok 1', '2026-05-07 01:16:40.995156', 'under evaluation', 1, 8.6021, 123.3921, 'leak', '2026-05-07 01:13:18.61106', 'Mark Joseph Macxilum Ligoro', 'https://www.facebook.com/profile.php?id=100033355176794');
INSERT INTO "public"."posts" VALUES (349, 'walay tubig daari sa bagting market road', '2026-05-07 01:16:40.997815', 'under evaluation', 4, 8.6142, 123.3987, 'no_water', '2026-05-07 01:13:18.61106', 'Mark Joseph Macxilum Ligoro', 'https://www.facebook.com/profile.php?id=100033355176794');
INSERT INTO "public"."posts" VALUES (350, 'buslot ang tubig daari sa bagting crossing street', '2026-05-07 01:16:40.999893', 'under evaluation', 4, 8.6142, 123.3987, 'leak', '2026-05-07 01:13:18.61106', 'Mark Joseph Macxilum Ligoro', 'https://www.facebook.com/profile.php?id=100033355176794');
INSERT INTO "public"."posts" VALUES (351, 'lubog ang tubig daari sa bagting market road', '2026-05-07 01:16:41.00182', 'under evaluation', 4, 8.6142, 123.3987, 'dirty_water', '2026-05-07 01:13:18.61106', 'Mark Joseph Macxilum Ligoro', 'https://www.facebook.com/profile.php?id=100033355176794');
INSERT INTO "public"."posts" VALUES (352, 'para asa ni na group?', '2026-05-07 01:16:41.003479', 'non-incident', NULL, NULL, NULL, 'Unknown', '2026-05-07 01:13:18.61106', 'Mark Joseph Macxilum Ligoro', 'https://www.facebook.com/profile.php?id=100033355176794');
INSERT INTO "public"."posts" VALUES (353, 'nako ang tubig dito sa Ilaya main road ang dumi', '2026-05-07 01:16:41.00593', 'under evaluation', 22, 8.6265, 123.413, 'dirty_water', '2026-05-07 01:13:18.61106', 'Mark Joseph Macxilum Ligoro', 'https://www.facebook.com/profile.php?id=100033355176794');
INSERT INTO "public"."posts" VALUES (354, 'way tubig wa Dawo purok farmers', '2026-05-07 01:16:41.007755', 'under evaluation', 19, 8.5985, 123.3889, 'no_water', '2026-05-07 01:13:18.61106', 'Mark Joseph Macxilum Ligoro', 'https://www.facebook.com/profile.php?id=100033355176794');
INSERT INTO "public"."posts" VALUES (355, 'wai agas Ilaya, upper crossing', '2026-05-07 01:16:41.010341', 'under evaluation', 22, 8.6265, 123.413, 'no_water', '2026-05-07 01:13:18.61106', 'Mark Joseph Macxilum Ligoro', 'https://www.facebook.com/profile.php?id=100033355176794');
INSERT INTO "public"."posts" VALUES (356, 'lubog ang tubig sa Larayan purok 5', '2026-05-07 01:16:41.013882', 'under evaluation', 25, 8.615, 123.405, 'dirty_water', '2026-05-07 01:13:18.61106', 'Mark Joseph Macxilum Ligoro', 'https://www.facebook.com/profile.php?id=100033355176794');
INSERT INTO "public"."posts" VALUES (357, 'madumi ang tubig dito sa bagting market road', '2026-05-07 01:16:41.015825', 'under evaluation', 4, 8.6142, 123.3987, 'dirty_water', '2026-05-07 01:13:18.61106', 'Mark Joseph Macxilum Ligoro', 'https://www.facebook.com/profile.php?id=100033355176794');
INSERT INTO "public"."posts" VALUES (358, 'walay agas daari sa bagting market road', '2026-05-07 01:16:41.017524', 'under evaluation', 4, 8.6142, 123.3987, 'no_water', '2026-05-07 01:13:18.61106', 'Mark Joseph Macxilum Ligoro', 'https://www.facebook.com/profile.php?id=100033355176794');
INSERT INTO "public"."posts" VALUES (359, 'hugay ang tubig daari sa bagting market road', '2026-05-07 01:16:41.019452', 'under evaluation', 4, 8.6142, 123.3987, 'dirty_water', '2026-05-07 01:13:18.61106', 'Mark Joseph Macxilum Ligoro', 'https://www.facebook.com/profile.php?id=100033355176794');
INSERT INTO "public"."posts" VALUES (360, 'wla lagi tubig daari sa bagting market road', '2026-05-07 01:16:41.021738', 'under evaluation', 4, 8.6142, 123.3987, 'no_water', '2026-05-07 01:13:18.61106', 'Mark Joseph Macxilum Ligoro', 'https://www.facebook.com/profile.php?id=100033355176794');
INSERT INTO "public"."posts" VALUES (361, 'hala lubog ang tubig sa bagting market road', '2026-05-07 01:16:41.023707', 'under evaluation', 4, 8.6142, 123.3987, 'dirty_water', '2026-05-07 01:13:18.61106', 'Mark Joseph Macxilum Ligoro', 'https://www.facebook.com/profile.php?id=100033355176794');
INSERT INTO "public"."posts" VALUES (362, 'hala naunsa mani', '2026-05-07 01:16:41.025111', 'non-incident', NULL, NULL, NULL, 'Unknown', '2026-05-07 01:13:18.61106', 'Mark Joseph Macxilum Ligoro', 'https://www.facebook.com/profile.php?id=100033355176794');
INSERT INTO "public"."posts" VALUES (365, 'tara valo', '2026-05-07 01:16:41.031234', 'false-report', 34, 8.6177, 123.4045, 'no_water', '2026-05-07 01:13:18.61106', 'Mark Joseph Macxilum Ligoro', 'https://www.facebook.com/profile.php?id=100033355176794');
INSERT INTO "public"."posts" VALUES (363, 'hugaw ang tubig daari sa bagting tungod sa market road', '2026-05-07 01:16:41.028284', 'completed', NULL, NULL, NULL, 'dirty_water', '2026-05-07 01:13:18.61106', 'Mark Joseph Macxilum Ligoro', 'https://www.facebook.com/profile.php?id=100033355176794');
INSERT INTO "public"."posts" VALUES (364, 'yoooooo valorant', '2026-05-07 01:16:41.029815', 'non-incident', NULL, NULL, NULL, 'Unknown', '2026-05-07 01:13:18.61106', 'Mark Joseph Macxilum Ligoro', 'https://www.facebook.com/profile.php?id=100033355176794');

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
INSERT INTO "public"."users" VALUES (4, 'manager', '123', 'manager', '2026-03-25 16:45:10.044306', NULL);
INSERT INTO "public"."users" VALUES (5, 'mark', '123', 'tubero', '2026-04-01 00:38:43.125256', 'markjosephligoro0@gmail.com');
INSERT INTO "public"."users" VALUES (6, 'actual tubero', '', 'tubero', '2026-05-07 05:53:37.536769', 'tub@gmail.com');
INSERT INTO "public"."users" VALUES (2, 'tubero', '123', 'tubero', '2026-03-11 05:29:25.151745', 'tuber@gmail.com');

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."incident_reports_id_seq"
OWNED BY "public"."incident_reports"."id";
SELECT setval('"public"."incident_reports_id_seq"', 100, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."keywords_id_seq"
OWNED BY "public"."keywords"."id";
SELECT setval('"public"."keywords_id_seq"', 114, true);

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
SELECT setval('"public"."posts_id_seq"', 365, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."users_id_seq"
OWNED BY "public"."users"."id";
SELECT setval('"public"."users_id_seq"', 6, true);

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
