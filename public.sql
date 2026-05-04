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

 Date: 04/05/2026 19:47:39
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
INSERT INTO "public"."incident_reports" VALUES (11035, -1, 5, 1, 8.682357, 123.333775, '2026-04-21 17:46:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11036, -1, 1, 1, 8.582001, 123.391202, '2026-04-14 13:02:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11037, -1, 7, 1, 8.723786, 123.413005, '2026-04-07 17:40:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11038, -1, 8, 1, 8.649692, 123.422835, '2026-03-31 15:04:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11039, -1, 5, 1, 8.567804, 123.460045, '2026-03-24 08:35:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11040, -1, 9, 1, 8.737799, 123.424907, '2026-03-17 09:13:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11041, -1, 5, 1, 8.661609, 123.500043, '2026-03-10 14:25:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11042, -1, 9, 1, 8.655565, 123.494987, '2026-03-03 16:46:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11043, -1, 7, 1, 8.694547, 123.449358, '2026-02-24 17:58:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11044, -1, 9, 1, 8.710378, 123.485443, '2026-02-17 13:54:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11045, -1, 9, 1, 8.631819, 123.405164, '2026-02-10 11:58:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11046, -1, 8, 1, 8.677407, 123.394661, '2026-02-03 18:46:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11047, -1, 5, 1, 8.598683, 123.483569, '2026-01-27 17:01:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11048, -1, 6, 1, 8.657107, 123.475265, '2026-01-20 10:44:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11049, -1, 8, 1, 8.72715, 123.387844, '2026-01-13 20:28:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11050, -1, 2, 1, 8.629016, 123.520258, '2026-01-06 18:41:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11051, -1, 3, 1, 8.670462, 123.492821, '2025-12-30 12:11:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11052, -1, 4, 1, 8.601256, 123.413698, '2025-12-23 11:07:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11053, -1, 7, 1, 8.679152, 123.322044, '2025-12-16 08:45:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11054, -1, 4, 1, 8.641368, 123.470071, '2025-12-09 19:03:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11055, -1, 9, 1, 8.608083, 123.481596, '2025-12-02 08:10:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11056, -1, 5, 1, 8.573602, 123.456239, '2025-11-25 13:47:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11057, -1, 1, 1, 8.727159, 123.550198, '2025-11-18 19:45:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11058, -1, 2, 1, 8.625001, 123.483212, '2025-11-11 16:47:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11059, -1, 4, 1, 8.634037, 123.389664, '2025-11-04 13:31:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11060, -1, 2, 1, 8.630007, 123.52926, '2025-10-28 16:19:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11061, -1, 1, 1, 8.611105, 123.46785, '2025-10-21 13:56:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11062, -1, 9, 1, 8.677622, 123.457157, '2025-10-14 13:17:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11063, -1, 3, 1, 8.665566, 123.407194, '2025-10-07 17:56:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11064, -1, 9, 1, 8.696417, 123.351017, '2025-09-30 19:51:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11065, -1, 1, 1, 8.654313, 123.327373, '2025-09-23 12:46:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11066, -1, 3, 1, 8.683587, 123.553464, '2025-09-16 11:32:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11067, -1, 6, 1, 8.640868, 123.327738, '2025-09-09 08:47:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11068, -1, 5, 1, 8.673745, 123.361902, '2025-09-02 20:53:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11069, -1, 1, 1, 8.610843, 123.344604, '2025-08-26 11:25:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11070, -1, 6, 1, 8.590664, 123.487048, '2025-08-19 14:27:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11071, -1, 6, 1, 8.62347, 123.447748, '2025-08-12 08:11:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11072, -1, 2, 1, 8.64847, 123.331218, '2025-08-05 08:20:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11073, -1, 4, 1, 8.698982, 123.330813, '2025-07-29 15:33:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11074, -1, 3, 1, 8.666979, 123.41051, '2025-07-22 08:11:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11075, -1, 4, 1, 8.6831, 123.303607, '2025-07-15 08:01:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11076, -1, 5, 1, 8.588253, 123.433778, '2025-07-08 08:18:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11077, -1, 1, 1, 8.602509, 123.499987, '2025-07-01 20:53:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11078, -1, 2, 1, 8.646075, 123.525013, '2025-06-24 16:44:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11079, -1, 7, 1, 8.640468, 123.552128, '2025-06-17 18:14:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11080, -1, 6, 1, 8.621059, 123.471929, '2025-06-10 08:38:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11081, -1, 7, 1, 8.711454, 123.405976, '2025-06-03 16:15:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11082, -1, 1, 1, 8.634446, 123.548275, '2025-05-27 19:21:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11083, -1, 1, 1, 8.720338, 123.4958, '2025-05-20 11:31:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11084, -1, 6, 1, 8.683203, 123.514249, '2025-05-13 16:39:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11085, -1, 9, 1, 8.67804, 123.532479, '2025-05-06 12:36:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11086, -1, 1, 1, 8.552354, 123.453512, '2025-04-29 10:30:40.990264', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11087, -1, 3, 1, 8.647973, 123.484237, '2026-04-21 19:55:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11088, -1, 9, 1, 8.599671, 123.3855, '2026-04-14 17:10:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11089, -1, 8, 1, 8.670472, 123.553008, '2026-04-07 13:45:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11090, -1, 9, 1, 8.574375, 123.366672, '2026-03-31 19:08:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11091, -1, 7, 1, 8.692384, 123.403179, '2026-03-24 14:42:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11092, -1, 5, 1, 8.678878, 123.318684, '2026-03-17 11:27:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11093, -1, 9, 1, 8.702599, 123.499733, '2026-03-10 09:47:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11094, -1, 2, 1, 8.560034, 123.454462, '2026-03-03 11:34:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11095, -1, 9, 1, 8.630595, 123.465773, '2026-02-24 13:18:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11096, -1, 4, 1, 8.696831, 123.373563, '2026-02-17 08:55:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11097, -1, 1, 1, 8.686083, 123.331391, '2026-02-10 10:52:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11098, -1, 1, 1, 8.57612, 123.317209, '2026-02-03 17:16:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11099, -1, 6, 1, 8.618451, 123.425189, '2026-01-27 16:40:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11100, -1, 3, 1, 8.658316, 123.509301, '2026-01-20 10:42:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11101, -1, 3, 1, 8.595303, 123.370611, '2026-01-13 16:29:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11102, -1, 2, 1, 8.716625, 123.474659, '2026-01-06 11:06:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11103, -1, 6, 1, 8.667558, 123.31044, '2025-12-30 19:48:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11104, -1, 1, 1, 8.6657, 123.521634, '2025-12-23 19:19:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11105, -1, 1, 1, 8.553405, 123.304681, '2025-12-16 11:43:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11106, -1, 4, 1, 8.638086, 123.308759, '2025-12-09 19:30:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11107, -1, 7, 1, 8.604831, 123.547632, '2025-12-02 09:26:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11108, -1, 1, 1, 8.613335, 123.472524, '2025-11-25 17:40:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11109, -1, 7, 1, 8.628956, 123.447116, '2025-11-18 17:46:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11110, -1, 4, 1, 8.684601, 123.511238, '2025-11-11 11:52:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11111, -1, 1, 1, 8.637271, 123.46654, '2025-11-04 20:47:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11112, -1, 6, 1, 8.683316, 123.322462, '2025-10-28 12:57:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11113, -1, 6, 1, 8.562054, 123.362907, '2025-10-21 18:12:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11114, -1, 2, 1, 8.598757, 123.417097, '2025-10-14 11:45:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11115, -1, 3, 1, 8.637399, 123.394197, '2025-10-07 16:57:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11116, -1, 9, 1, 8.649181, 123.503985, '2025-09-30 13:52:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11117, -1, 5, 1, 8.675376, 123.378458, '2025-09-23 11:20:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11118, -1, 2, 1, 8.560098, 123.415003, '2025-09-16 13:13:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11119, -1, 3, 1, 8.693234, 123.373625, '2025-09-09 12:51:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11120, -1, 8, 1, 8.549828, 123.431907, '2025-09-02 16:17:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11121, -1, 7, 1, 8.737234, 123.402614, '2025-08-26 08:53:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11122, -1, 3, 1, 8.662876, 123.385294, '2025-08-19 12:52:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11123, -1, 8, 1, 8.569355, 123.330251, '2025-08-12 15:25:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11124, -1, 8, 1, 8.709472, 123.477732, '2025-08-05 10:24:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11125, -1, 6, 1, 8.631124, 123.516095, '2025-07-29 16:10:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11126, -1, 9, 1, 8.638411, 123.453307, '2025-07-22 16:37:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11127, -1, 8, 1, 8.610513, 123.443036, '2025-07-15 14:01:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11128, -1, 5, 1, 8.652466, 123.363963, '2025-07-08 16:10:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11129, -1, 5, 1, 8.680611, 123.381516, '2025-07-01 13:21:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11130, -1, 8, 1, 8.662397, 123.528656, '2025-06-24 19:10:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11131, -1, 4, 1, 8.670568, 123.436637, '2025-06-17 12:09:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11132, -1, 5, 1, 8.694849, 123.453832, '2025-06-10 16:11:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11133, -1, 3, 1, 8.647281, 123.356444, '2025-06-03 10:57:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11134, -1, 9, 1, 8.64396, 123.495299, '2025-05-27 13:49:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11135, -1, 8, 1, 8.635532, 123.447369, '2025-05-20 18:34:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11136, -1, 9, 1, 8.619266, 123.473493, '2025-05-13 08:52:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11137, -1, 1, 1, 8.693107, 123.435549, '2025-05-06 12:13:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11138, -1, 3, 1, 8.586136, 123.312524, '2025-04-29 14:51:11.222636', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11139, -1, 9, 15, 8.628172, 123.40024, '2026-04-21 20:02:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11140, -1, 9, 15, 8.684893, 123.415415, '2026-04-14 19:26:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11141, -1, 9, 15, 8.640452, 123.363711, '2026-04-07 10:50:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11142, -1, 7, 15, 8.734004, 123.548751, '2026-03-31 16:01:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11143, -1, 7, 15, 8.61307, 123.527813, '2026-03-24 20:06:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11144, -1, 7, 15, 8.554137, 123.538739, '2026-03-17 11:21:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11145, -1, 2, 15, 8.642601, 123.445528, '2026-03-10 17:07:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11146, -1, 1, 15, 8.652278, 123.413082, '2026-03-03 08:02:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11147, -1, 8, 15, 8.689105, 123.475785, '2026-02-24 08:41:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11148, -1, 1, 15, 8.694675, 123.350826, '2026-02-17 11:19:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11149, -1, 8, 15, 8.612401, 123.446769, '2026-02-10 15:04:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11150, -1, 2, 15, 8.675295, 123.395781, '2026-02-03 08:44:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11151, -1, 3, 15, 8.644118, 123.313421, '2026-01-27 12:33:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11152, -1, 7, 15, 8.630239, 123.474088, '2026-01-20 20:15:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11153, -1, 4, 15, 8.570321, 123.499853, '2026-01-13 08:23:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11154, -1, 2, 15, 8.565903, 123.546403, '2026-01-06 13:27:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11155, -1, 1, 15, 8.679508, 123.448844, '2025-12-30 12:32:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11156, -1, 6, 15, 8.730998, 123.494618, '2025-12-23 09:15:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11157, -1, 4, 15, 8.678257, 123.497488, '2025-12-16 16:07:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11158, -1, 1, 15, 8.665321, 123.389555, '2025-12-09 15:42:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11159, -1, 8, 15, 8.641808, 123.527382, '2025-12-02 19:54:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11160, -1, 8, 15, 8.626627, 123.474625, '2025-11-25 12:07:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11161, -1, 7, 15, 8.572093, 123.544373, '2025-11-18 20:36:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11162, -1, 8, 15, 8.627279, 123.539784, '2025-11-11 16:46:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11163, -1, 9, 15, 8.692093, 123.366142, '2025-11-04 08:44:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11164, -1, 3, 15, 8.566157, 123.481714, '2025-10-28 18:23:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11165, -1, 9, 15, 8.654703, 123.339754, '2025-10-21 10:45:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11166, -1, 3, 15, 8.688786, 123.444829, '2025-10-14 14:53:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11167, -1, 4, 15, 8.689173, 123.43595, '2025-10-07 12:42:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11168, -1, 4, 15, 8.663068, 123.405184, '2025-09-30 13:41:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11169, -1, 2, 15, 8.675436, 123.313656, '2025-09-23 10:13:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11170, -1, 9, 15, 8.643773, 123.375641, '2025-09-16 13:37:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11171, -1, 9, 15, 8.668246, 123.517051, '2025-09-09 16:04:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11172, -1, 5, 15, 8.71769, 123.344044, '2025-09-02 09:38:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11173, -1, 6, 15, 8.653764, 123.39634, '2025-08-26 18:58:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11174, -1, 3, 15, 8.634055, 123.359121, '2025-08-19 11:02:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11175, -1, 9, 15, 8.603252, 123.427712, '2025-08-12 19:55:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11176, -1, 2, 15, 8.609256, 123.469274, '2025-08-05 11:21:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11177, -1, 5, 15, 8.729711, 123.424363, '2025-07-29 12:13:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11178, -1, 5, 15, 8.703571, 123.401167, '2025-07-22 11:43:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11179, -1, 9, 15, 8.652885, 123.476229, '2025-07-15 18:49:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11180, -1, 3, 15, 8.674666, 123.501713, '2025-07-08 15:29:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11181, -1, 4, 15, 8.603872, 123.322598, '2025-07-01 20:30:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11182, -1, 4, 15, 8.640019, 123.53034, '2025-06-24 20:31:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11183, -1, 6, 15, 8.637734, 123.413349, '2025-06-17 10:23:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11184, -1, 9, 15, 8.687006, 123.32524, '2025-06-10 17:58:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11185, -1, 2, 15, 8.700433, 123.436647, '2025-06-03 12:08:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11186, -1, 9, 15, 8.699043, 123.318201, '2025-05-27 10:29:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11187, -1, 8, 15, 8.636943, 123.374665, '2025-05-20 18:10:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11188, -1, 8, 15, 8.736238, 123.377002, '2025-05-13 10:57:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11189, -1, 3, 15, 8.687464, 123.407678, '2025-05-06 18:27:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11190, -1, 7, 15, 8.608415, 123.403711, '2025-04-29 19:49:59.414738', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11191, -1, 1, 15, 8.713311, 123.55099, '2026-04-21 17:26:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11192, -1, 1, 15, 8.707889, 123.491471, '2026-04-14 08:30:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11193, -1, 6, 15, 8.689545, 123.358021, '2026-04-07 08:59:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11194, -1, 8, 15, 8.725347, 123.399401, '2026-03-31 18:57:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11195, -1, 1, 15, 8.599717, 123.384944, '2026-03-24 10:08:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11196, -1, 2, 15, 8.69286, 123.325473, '2026-03-17 19:52:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11197, -1, 2, 15, 8.596682, 123.344494, '2026-03-10 12:27:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11198, -1, 3, 15, 8.676698, 123.360178, '2026-03-03 13:08:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11199, -1, 5, 15, 8.717817, 123.341159, '2026-02-24 18:47:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11200, -1, 5, 15, 8.651389, 123.502146, '2026-02-17 08:41:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11201, -1, 8, 15, 8.662467, 123.441283, '2026-02-10 10:00:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11202, -1, 1, 15, 8.704119, 123.304363, '2026-02-03 12:09:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11203, -1, 2, 15, 8.676617, 123.327055, '2026-01-27 19:02:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11204, -1, 6, 15, 8.605272, 123.491983, '2026-01-20 10:04:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11205, -1, 7, 15, 8.551203, 123.362317, '2026-01-13 13:25:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11206, -1, 4, 15, 8.609885, 123.357027, '2026-01-06 16:50:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11207, -1, 1, 15, 8.625895, 123.41571, '2025-12-30 11:33:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11208, -1, 7, 15, 8.614965, 123.456684, '2025-12-23 09:59:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11209, -1, 7, 15, 8.713692, 123.443288, '2025-12-16 12:22:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11210, -1, 2, 15, 8.554891, 123.312629, '2025-12-09 13:30:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11211, -1, 6, 15, 8.686354, 123.310103, '2025-12-02 13:55:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11212, -1, 9, 15, 8.687549, 123.54269, '2025-11-25 12:03:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11213, -1, 4, 15, 8.66435, 123.51994, '2025-11-18 15:29:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11214, -1, 8, 15, 8.643055, 123.410238, '2025-11-11 16:07:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11215, -1, 1, 15, 8.642904, 123.349015, '2025-11-04 08:51:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11216, -1, 4, 15, 8.662274, 123.523312, '2025-10-28 12:20:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11217, -1, 9, 15, 8.576616, 123.478571, '2025-10-21 13:24:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11218, -1, 2, 15, 8.623457, 123.412931, '2025-10-14 08:00:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11219, -1, 8, 15, 8.697794, 123.416568, '2025-10-07 19:55:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11220, -1, 1, 15, 8.672448, 123.519501, '2025-09-30 16:21:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11221, -1, 2, 15, 8.616391, 123.499135, '2025-09-23 15:30:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11222, -1, 2, 15, 8.620414, 123.401303, '2025-09-16 11:17:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11223, -1, 8, 15, 8.707208, 123.458927, '2025-09-09 20:18:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11224, -1, 2, 15, 8.581691, 123.541877, '2025-09-02 13:03:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11225, -1, 4, 15, 8.594015, 123.327695, '2025-08-26 12:52:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11226, -1, 7, 15, 8.636661, 123.534066, '2025-08-19 17:14:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11227, -1, 9, 15, 8.601357, 123.461824, '2025-08-12 17:26:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11228, -1, 4, 15, 8.613578, 123.437802, '2025-08-05 15:05:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11229, -1, 5, 15, 8.689265, 123.336935, '2025-07-29 12:30:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11230, -1, 2, 15, 8.713292, 123.456534, '2025-07-22 16:49:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11231, -1, 1, 15, 8.687768, 123.534074, '2025-07-15 12:23:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11232, -1, 6, 15, 8.623079, 123.381777, '2025-07-08 13:23:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11233, -1, 8, 15, 8.580721, 123.491394, '2025-07-01 13:40:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11234, -1, 5, 15, 8.681254, 123.379792, '2025-06-24 08:00:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11235, -1, 8, 15, 8.618405, 123.486007, '2025-06-17 20:18:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11236, -1, 8, 15, 8.700005, 123.410728, '2025-06-10 20:17:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11237, -1, 7, 15, 8.63724, 123.5504, '2025-06-03 20:51:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11238, -1, 9, 15, 8.668313, 123.499024, '2025-05-27 15:07:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11239, -1, 8, 15, 8.550582, 123.343386, '2025-05-20 13:31:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11240, -1, 3, 15, 8.571955, 123.434844, '2025-05-13 17:59:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11241, -1, 6, 15, 8.576901, 123.514099, '2025-05-06 09:26:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11242, -1, 5, 15, 8.720565, 123.338536, '2025-04-29 09:31:31.598593', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11243, -1, 7, 15, 8.72397, 123.472647, '2026-04-21 11:43:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11244, -1, 6, 15, 8.570493, 123.5256, '2026-04-14 08:33:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11245, -1, 3, 15, 8.695996, 123.410041, '2026-04-07 12:54:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11246, -1, 1, 15, 8.736142, 123.361604, '2026-03-31 14:00:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11247, -1, 9, 15, 8.551796, 123.494397, '2026-03-24 09:58:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11248, -1, 5, 15, 8.642763, 123.551889, '2026-03-17 19:13:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11249, -1, 8, 15, 8.678364, 123.32208, '2026-03-10 17:39:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11250, -1, 1, 15, 8.589968, 123.321055, '2026-03-03 11:12:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11251, -1, 5, 15, 8.559601, 123.361218, '2026-02-24 15:24:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11252, -1, 3, 15, 8.705151, 123.545316, '2026-02-17 10:55:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11253, -1, 6, 15, 8.602448, 123.344958, '2026-02-10 18:32:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11254, -1, 2, 15, 8.627272, 123.459312, '2026-02-03 09:08:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11255, -1, 4, 15, 8.557943, 123.53774, '2026-01-27 20:24:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11256, -1, 3, 15, 8.715509, 123.432292, '2026-01-20 14:18:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11257, -1, 2, 15, 8.738201, 123.422907, '2026-01-13 19:24:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11258, -1, 2, 15, 8.727399, 123.488649, '2026-01-06 13:42:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11259, -1, 2, 15, 8.567104, 123.363614, '2025-12-30 10:36:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11260, -1, 6, 15, 8.662781, 123.509707, '2025-12-23 13:49:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11261, -1, 1, 15, 8.578869, 123.378855, '2025-12-16 13:21:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11262, -1, 4, 15, 8.558593, 123.532696, '2025-12-09 12:44:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11263, -1, 7, 15, 8.588774, 123.50032, '2025-12-02 18:39:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11264, -1, 8, 15, 8.688877, 123.424372, '2025-11-25 16:41:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11265, -1, 1, 15, 8.570837, 123.489962, '2025-11-18 08:46:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11266, -1, 9, 15, 8.588009, 123.30613, '2025-11-11 11:05:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11267, -1, 3, 15, 8.722042, 123.526407, '2025-11-04 15:42:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11268, -1, 4, 15, 8.582201, 123.316404, '2025-10-28 10:00:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11269, -1, 5, 15, 8.646615, 123.320956, '2025-10-21 13:38:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11270, -1, 6, 15, 8.678659, 123.377827, '2025-10-14 12:29:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11271, -1, 4, 15, 8.665332, 123.400065, '2025-10-07 09:27:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11272, -1, 5, 15, 8.601953, 123.429627, '2025-09-30 14:24:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11273, -1, 8, 15, 8.577518, 123.480291, '2025-09-23 13:52:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11274, -1, 9, 15, 8.58069, 123.383934, '2025-09-16 16:56:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11275, -1, 4, 15, 8.636022, 123.548312, '2025-09-09 10:21:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11276, -1, 4, 15, 8.575356, 123.384769, '2025-09-02 16:08:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11277, -1, 7, 15, 8.709543, 123.306829, '2025-08-26 13:59:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11278, -1, 8, 15, 8.610238, 123.538823, '2025-08-19 19:47:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11279, -1, 5, 15, 8.687638, 123.457572, '2025-08-12 19:07:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11280, -1, 5, 15, 8.699349, 123.33092, '2025-08-05 15:30:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11281, -1, 7, 15, 8.58045, 123.499835, '2025-07-29 09:07:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11282, -1, 1, 15, 8.680132, 123.316468, '2025-07-22 08:02:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11283, -1, 7, 15, 8.564136, 123.356561, '2025-07-15 13:56:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11284, -1, 5, 15, 8.565715, 123.508776, '2025-07-08 17:16:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11285, -1, 2, 15, 8.679489, 123.477303, '2025-07-01 10:16:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11286, -1, 9, 15, 8.707332, 123.475937, '2025-06-24 12:59:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11287, -1, 9, 15, 8.662917, 123.518664, '2025-06-17 18:40:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11288, -1, 7, 15, 8.635489, 123.366443, '2025-06-10 17:43:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11289, -1, 1, 15, 8.606826, 123.312227, '2025-06-03 12:57:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11290, -1, 7, 15, 8.586801, 123.366876, '2025-05-27 20:32:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11291, -1, 1, 15, 8.55502, 123.526453, '2025-05-20 14:20:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11292, -1, 8, 15, 8.586141, 123.453095, '2025-05-13 15:14:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11293, -1, 4, 15, 8.628727, 123.407041, '2025-05-06 13:20:42.703021', 'High Priority', 'Pending');
INSERT INTO "public"."incident_reports" VALUES (11294, -1, 7, 15, 8.64925, 123.497756, '2025-04-29 12:46:42.703021', 'High Priority', 'Pending');

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
  "date_scraped" timestamp(6) DEFAULT now(),
  "status" varchar(255) COLLATE "pg_catalog"."default",
  "location_id" int4,
  "latitude" float8,
  "longitude" float8,
  "nlp_intent" varchar(255) COLLATE "pg_catalog"."default",
  "nlp_score" varchar(255) COLLATE "pg_catalog"."default",
  "scraper_init" timestamp(6)
)
;

-- ----------------------------
-- Records of posts
-- ----------------------------

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
INSERT INTO "public"."users" VALUES (4, 'manager', '123', 'manager', '2026-03-25 16:45:10.044306', NULL);
INSERT INTO "public"."users" VALUES (5, 'mark', '123', 'tubero', '2026-04-01 00:38:43.125256', 'markjosephligoro0@gmail.com');

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."incident_reports_id_seq"
OWNED BY "public"."incident_reports"."id";
SELECT setval('"public"."incident_reports_id_seq"', 11398, true);

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
SELECT setval('"public"."posts_id_seq"', 82, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."users_id_seq"
OWNED BY "public"."users"."id";
SELECT setval('"public"."users_id_seq"', 5, true);

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
