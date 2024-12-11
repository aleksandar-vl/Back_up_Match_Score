--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
--

INSERT INTO public."user" VALUES ('admin@kitten.com', '$2b$12$496sAD.GDbIGw2PJkL21H.GtTnry2/6LyxQZJZu7nOLMvTZGmJTcO', 'ADMIN', '2024-11-27 10:54:39.123306+02', 'e1111111-1111-4111-1111-111111111111');
INSERT INTO public."user" VALUES ('director@kitten.com', '$2b$12$496sAD.GDbIGw2PJkL21H.GtTnry2/6LyxQZJZu7nOLMvTZGmJTcO', 'DIRECTOR', '2024-11-27 10:54:39.123306+02', 'e2222222-2222-4222-2222-222222222222');
INSERT INTO public."user" VALUES ('user@kitten.com', '$2b$12$496sAD.GDbIGw2PJkL21H.GtTnry2/6LyxQZJZu7nOLMvTZGmJTcO', 'USER', '2024-11-27 10:54:39.123306+02', 'e3333333-3333-4333-3333-333333333333');
INSERT INTO public."user" VALUES ('whiskers.hunter@kitten.com', '$2b$12$496sAD.GDbIGw2PJkL21H.GtTnry2/6LyxQZJZu7nOLMvTZGmJTcO', 'USER', '2024-11-27 11:00:39.123306+02', 'e4444444-4444-4444-4444-444444444444');
INSERT INTO public."user" VALUES ('paw.striker@kitten.com', '$2b$12$496sAD.GDbIGw2PJkL21H.GtTnry2/6LyxQZJZu7nOLMvTZGmJTcO', 'USER', '2024-11-27 11:15:39.123306+02', 'e5555555-5555-4555-5555-555555555555');
INSERT INTO public."user" VALUES ('ninja.cat@kitten.com', '$2b$12$496sAD.GDbIGw2PJkL21H.GtTnry2/6LyxQZJZu7nOLMvTZGmJTcO', 'USER', '2024-11-27 11:30:39.123306+02', 'e6666666-6666-4666-6666-666666666666');
INSERT INTO public."user" VALUES ('meow.master@kitten.com', '$2b$12$496sAD.GDbIGw2PJkL21H.GtTnry2/6LyxQZJZu7nOLMvTZGmJTcO', 'USER', '2024-11-27 11:45:39.123306+02', 'e7777777-7777-4777-7777-777777777777');
INSERT INTO public."user" VALUES ('purr.pro@kitten.com', '$2b$12$496sAD.GDbIGw2PJkL21H.GtTnry2/6LyxQZJZu7nOLMvTZGmJTcO', 'USER', '2024-11-27 12:00:39.123306+02', 'e8888888-8888-4888-8888-888888888888');


--
--

INSERT INTO public.tournament VALUES ('Whiskers Cup 2024', 'SINGLE_ELIMINATION', '2024-01-15 10:00:00', '2024-01-16 18:00:00', 10000, 'FINISHED', 'e2222222-2222-4222-2222-222222222222', 'a1111111-1111-4111-1111-111111111111');
INSERT INTO public.tournament VALUES ('Yarn Ball League Season 1', 'ROUND_ROBIN', '2023-12-01 12:00:00', '2023-12-03 18:00:00', 12000, 'FINISHED', 'e2222222-2222-4222-2222-222222222222', 'a4444444-4444-4444-4444-444444444444');
INSERT INTO public.tournament VALUES ('Kitten Strike Winter Cup', 'SINGLE_ELIMINATION', '2023-11-01 10:00:00', '2023-11-02 20:00:00', 8000, 'FINISHED', 'e2222222-2222-4222-2222-222222222222', 'a5555555-5555-4555-5555-555555555555');
INSERT INTO public.tournament VALUES ('Meow Masters Fall', 'ROUND_ROBIN', '2023-10-01 11:00:00', '2023-10-03 19:00:00', 15000, 'FINISHED', 'e2222222-2222-4222-2222-222222222222', 'a6666666-6666-4666-6666-666666666666');
INSERT INTO public.tournament VALUES ('Pawsome Championship 2023', 'SINGLE_ELIMINATION', '2023-09-15 09:00:00', '2023-09-25 21:00:00', 18000, 'FINISHED', 'e2222222-2222-4222-2222-222222222222', 'a7777777-7777-4777-7777-777777777777');
INSERT INTO public.tournament VALUES ('Catnip Masters', 'ROUND_ROBIN', '2024-12-11 11:00:00', '2024-12-13 20:00:00', 15000, 'GROUP_STAGE', 'e2222222-2222-4222-2222-222222222222', 'a2222222-2222-4222-2222-222222222222');
INSERT INTO public.tournament VALUES ('Feline Frenzy Cup', 'SINGLE_ELIMINATION', '2024-12-11 10:00:00', '2024-12-11 18:00:00', 13000, 'FINAL', 'e2222222-2222-4222-2222-222222222222', 'a8888888-8888-4888-8888-888888888888');
INSERT INTO public.tournament VALUES ('Paw Champions League', 'ONE_OFF_MATCH', '2024-12-12 08:00:00', '2024-12-12 23:00:00', 20000, 'FINAL', 'e2222222-2222-4222-2222-222222222222', 'a3333333-3333-4333-3333-333333333333');
INSERT INTO public.tournament VALUES ('Scratch Masters Spring', 'ONE_OFF_MATCH', '2025-01-15 11:00:00', '2025-01-15 23:00:00', 16000, 'FINAL', 'e2222222-2222-4222-2222-222222222222', 'a9999999-9999-4999-9999-999999999999');


--
--

INSERT INTO public.team VALUES ('Feline Fury', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/teams/20241127_112924_558c7135.png', 10, 4, NULL, 'f1111111-1111-4111-1111-111111111111');
INSERT INTO public.team VALUES ('Whisker Warriors', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/teams/20241127_112947_4ceaf52c.png', 20, 12, 'a2222222-2222-4222-2222-222222222222', 'f2222222-2222-4222-2222-222222222222');
INSERT INTO public.team VALUES ('Catnip Commandos', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/teams/20241127_113027_f0d43893.png', 18, 8, 'a8888888-8888-4888-8888-888888888888', 'f3333333-3333-4333-3333-333333333333');
INSERT INTO public.team VALUES ('Paw Patrol Elite', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/teams/20241127_120053_730211b4.png', 12, 6, 'a3333333-3333-4333-3333-333333333333', 'f5555555-5555-4555-5555-555555555555');
INSERT INTO public.team VALUES ('Purr-fessionals', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/teams/20241127_121958_72ec0ad7.png', 25, 18, 'a8888888-8888-4888-8888-888888888888', 'f6666666-6666-4666-6666-666666666666');
INSERT INTO public.team VALUES ('Meow Mercenaries', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/teams/20241127_122112_7d1a9efe.png', 8, 3, 'a3333333-3333-4333-3333-333333333333', 'f7777777-7777-4777-7777-777777777777');
INSERT INTO public.team VALUES ('Scratch Squadron', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/teams/20241127_122141_d56358c1.png', 22, 15, 'a9999999-9999-4999-9999-999999999999', 'f8888888-8888-4888-8888-888888888888');
INSERT INTO public.team VALUES ('Yarn Yeeters', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/teams/20241127_122211_3a9e30c8.png', 14, 6, 'a2222222-2222-4222-2222-222222222222', 'f9999999-9999-4999-9999-999999999999');
INSERT INTO public.team VALUES ('Kitty Kombatants', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/teams/20241127_122247_92915713.png', 16, 9, 'a9999999-9999-4999-9999-999999999999', 'faaaaaaa-aaaa-4aaa-aaaa-aaaaaaaaaaaa');
INSERT INTO public.team VALUES ('Purrito Patriots', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/teams/20241127_122301_e87b2c4e.png', 19, 11, 'a2222222-2222-4222-2222-222222222222', 'fbbbbbbb-bbbb-4bbb-bbbb-bbbbbbbbbbbb');
INSERT INTO public.team VALUES ('Nyan Ninjas', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/teams/20241127_122321_1c97cf42.png', 13, 5, NULL, 'fccccccc-cccc-4ccc-cccc-cccccccccccc');
INSERT INTO public.team VALUES ('Mittens of Mayhem', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/teams/20241127_122343_f6d548b5.png', 15, 7, 'a2222222-2222-4222-2222-222222222222', 'f4444444-4444-4444-4444-444444444444');


--
--

INSERT INTO public.match VALUES ('MR15', '2024-01-15 11:00:00', true, 'SEMI_FINAL', 'f1111111-1111-4111-1111-111111111111', 'f2222222-2222-4222-2222-222222222222', 16, 14, 'f1111111-1111-4111-1111-111111111111', 'a1111111-1111-4111-1111-111111111111', 'c1111111-1111-4111-1111-111111111111');
INSERT INTO public.match VALUES ('MR15', '2024-01-15 14:00:00', true, 'SEMI_FINAL', 'f3333333-3333-4333-3333-333333333333', 'f6666666-6666-4666-6666-666666666666', 13, 16, 'f6666666-6666-4666-6666-666666666666', 'a1111111-1111-4111-1111-111111111111', 'c2222222-2222-4222-2222-222222222222');
INSERT INTO public.match VALUES ('MR15', '2024-01-16 11:00:00', true, 'FINAL', 'f1111111-1111-4111-1111-111111111111', 'f6666666-6666-4666-6666-666666666666', 16, 12, 'f1111111-1111-4111-1111-111111111111', 'a1111111-1111-4111-1111-111111111111', 'c3333333-3333-4333-3333-333333333333');
INSERT INTO public.match VALUES ('MR12', '2023-12-01 11:00:00', true, 'GROUP_STAGE', 'f2222222-2222-4222-2222-222222222222', 'f3333333-3333-4333-3333-333333333333', 13, 9, 'f2222222-2222-4222-2222-222222222222', 'a4444444-4444-4444-4444-444444444444', 'ca111111-1111-4111-1111-111111111111');
INSERT INTO public.match VALUES ('MR12', '2023-12-01 14:00:00', true, 'GROUP_STAGE', 'f7777777-7777-4777-7777-777777777777', 'fccccccc-cccc-4ccc-cccc-cccccccccccc', 13, 11, 'f7777777-7777-4777-7777-777777777777', 'a4444444-4444-4444-4444-444444444444', 'ca222222-2222-4222-2222-222222222222');
INSERT INTO public.match VALUES ('MR12', '2023-12-01 17:00:00', true, 'GROUP_STAGE', 'f2222222-2222-4222-2222-222222222222', 'f7777777-7777-4777-7777-777777777777', 13, 7, 'f2222222-2222-4222-2222-222222222222', 'a4444444-4444-4444-4444-444444444444', 'ca333333-3333-4333-3333-333333333333');
INSERT INTO public.match VALUES ('MR12', '2023-12-01 20:00:00', true, 'GROUP_STAGE', 'f3333333-3333-4333-3333-333333333333', 'fccccccc-cccc-4ccc-cccc-cccccccccccc', 13, 10, 'f3333333-3333-4333-3333-333333333333', 'a4444444-4444-4444-4444-444444444444', 'ca444444-4444-4444-4444-444444444444');
INSERT INTO public.match VALUES ('MR12', '2023-12-02 11:00:00', true, 'GROUP_STAGE', 'f2222222-2222-4222-2222-222222222222', 'fccccccc-cccc-4ccc-cccc-cccccccccccc', 13, 8, 'f2222222-2222-4222-2222-222222222222', 'a4444444-4444-4444-4444-444444444444', 'ca555555-5555-4555-5555-555555555555');
INSERT INTO public.match VALUES ('MR12', '2023-12-02 14:00:00', true, 'GROUP_STAGE', 'f3333333-3333-4333-3333-333333333333', 'f7777777-7777-4777-7777-777777777777', 9, 13, 'f7777777-7777-4777-7777-777777777777', 'a4444444-4444-4444-4444-444444444444', 'ca666666-6666-4666-6666-666666666666');
INSERT INTO public.match VALUES ('MR15', '2023-12-03 11:00:00', true, 'FINAL', 'f2222222-2222-4222-2222-222222222222', 'f7777777-7777-4777-7777-777777777777', 16, 11, 'f2222222-2222-4222-2222-222222222222', 'a4444444-4444-4444-4444-444444444444', 'ca777777-7777-4777-7777-777777777777');
INSERT INTO public.match VALUES ('MR15', '2023-11-01 11:00:00', true, 'SEMI_FINAL', 'f8888888-8888-4888-8888-888888888888', 'f7777777-7777-4777-7777-777777777777', 16, 10, 'f8888888-8888-4888-8888-888888888888', 'a5555555-5555-4555-5555-555555555555', 'c4444444-4444-4444-4444-444444444444');
INSERT INTO public.match VALUES ('MR15', '2023-11-01 14:00:00', true, 'SEMI_FINAL', 'f4444444-4444-4444-4444-444444444444', 'faaaaaaa-aaaa-4aaa-aaaa-aaaaaaaaaaaa', 16, 13, 'f4444444-4444-4444-4444-444444444444', 'a5555555-5555-4555-5555-555555555555', 'c5555555-5555-4555-5555-555555555555');
INSERT INTO public.match VALUES ('MR15', '2023-11-02 11:00:00', true, 'FINAL', 'f8888888-8888-4888-8888-888888888888', 'f4444444-4444-4444-4444-444444444444', 16, 14, 'f8888888-8888-4888-8888-888888888888', 'a5555555-5555-4555-5555-555555555555', 'c6666666-6666-4666-6666-666666666666');
INSERT INTO public.match VALUES ('MR12', '2023-10-01 11:00:00', true, 'GROUP_STAGE', 'f1111111-1111-4111-1111-111111111111', 'f5555555-5555-4555-5555-555555555555', 13, 10, 'f1111111-1111-4111-1111-111111111111', 'a6666666-6666-4666-6666-666666666666', 'cb111111-1111-4111-1111-111111111111');
INSERT INTO public.match VALUES ('MR12', '2023-10-01 14:00:00', true, 'GROUP_STAGE', 'f8888888-8888-4888-8888-888888888888', 'faaaaaaa-aaaa-4aaa-aaaa-aaaaaaaaaaaa', 13, 8, 'f8888888-8888-4888-8888-888888888888', 'a6666666-6666-4666-6666-666666666666', 'cb222222-2222-4222-2222-222222222222');
INSERT INTO public.match VALUES ('MR12', '2023-10-01 17:00:00', true, 'GROUP_STAGE', 'f1111111-1111-4111-1111-111111111111', 'f8888888-8888-4888-8888-888888888888', 11, 13, 'f8888888-8888-4888-8888-888888888888', 'a6666666-6666-4666-6666-666666666666', 'cb333333-3333-4333-3333-333333333333');
INSERT INTO public.match VALUES ('MR12', '2023-10-01 20:00:00', true, 'GROUP_STAGE', 'f5555555-5555-4555-5555-555555555555', 'faaaaaaa-aaaa-4aaa-aaaa-aaaaaaaaaaaa', 13, 11, 'f5555555-5555-4555-5555-555555555555', 'a6666666-6666-4666-6666-666666666666', 'cb444444-4444-4444-4444-444444444444');
INSERT INTO public.match VALUES ('MR12', '2023-10-02 11:00:00', true, 'GROUP_STAGE', 'f1111111-1111-4111-1111-111111111111', 'faaaaaaa-aaaa-4aaa-aaaa-aaaaaaaaaaaa', 13, 9, 'f1111111-1111-4111-1111-111111111111', 'a6666666-6666-4666-6666-666666666666', 'cb555555-5555-4555-5555-555555555555');
INSERT INTO public.match VALUES ('MR12', '2023-10-02 14:00:00', true, 'GROUP_STAGE', 'f5555555-5555-4555-5555-555555555555', 'f8888888-8888-4888-8888-888888888888', 7, 13, 'f8888888-8888-4888-8888-888888888888', 'a6666666-6666-4666-6666-666666666666', 'cb666666-6666-4666-6666-666666666666');
INSERT INTO public.match VALUES ('MR15', '2023-10-03 11:00:00', true, 'FINAL', 'f8888888-8888-4888-8888-888888888888', 'f1111111-1111-4111-1111-111111111111', 16, 14, 'f8888888-8888-4888-8888-888888888888', 'a6666666-6666-4666-6666-666666666666', 'cb777777-7777-4777-7777-777777777777');
INSERT INTO public.match VALUES ('MR15', '2023-09-15 11:00:00', true, 'SEMI_FINAL', 'f6666666-6666-4666-6666-666666666666', 'f9999999-9999-4999-9999-999999999999', 16, 11, 'f6666666-6666-4666-6666-666666666666', 'a7777777-7777-4777-7777-777777777777', 'c7777777-7777-4777-7777-777777777777');
INSERT INTO public.match VALUES ('MR15', '2023-09-15 14:00:00', true, 'SEMI_FINAL', 'fbbbbbbb-bbbb-4bbb-bbbb-bbbbbbbbbbbb', 'fccccccc-cccc-4ccc-cccc-cccccccccccc', 16, 9, 'fbbbbbbb-bbbb-4bbb-bbbb-bbbbbbbbbbbb', 'a7777777-7777-4777-7777-777777777777', 'c8888888-8888-4888-8888-888888888888');
INSERT INTO public.match VALUES ('MR15', '2023-09-16 11:00:00', true, 'FINAL', 'f6666666-6666-4666-6666-666666666666', 'fbbbbbbb-bbbb-4bbb-bbbb-bbbbbbbbbbbb', 16, 13, 'f6666666-6666-4666-6666-666666666666', 'a7777777-7777-4777-7777-777777777777', 'c9999999-9999-4999-9999-999999999999');
INSERT INTO public.match VALUES ('MR12', '2024-12-11 11:00:00', true, 'GROUP_STAGE', 'fbbbbbbb-bbbb-4bbb-bbbb-bbbbbbbbbbbb', 'f9999999-9999-4999-9999-999999999999', 13, 9, 'fbbbbbbb-bbbb-4bbb-bbbb-bbbbbbbbbbbb', 'a2222222-2222-4222-2222-222222222222', 'cc111111-1111-4111-1111-111111111111');
INSERT INTO public.match VALUES ('MR12', '2024-12-11 14:00:00', true, 'GROUP_STAGE', 'f4444444-4444-4444-4444-444444444444', 'f2222222-2222-4222-2222-222222222222', 13, 11, 'f4444444-4444-4444-4444-444444444444', 'a2222222-2222-4222-2222-222222222222', 'cc222222-2222-4222-2222-222222222222');
INSERT INTO public.match VALUES ('MR12', '2024-12-11 17:00:00', true, 'GROUP_STAGE', 'fbbbbbbb-bbbb-4bbb-bbbb-bbbbbbbbbbbb', 'f4444444-4444-4444-4444-444444444444', 10, 13, 'f4444444-4444-4444-4444-444444444444', 'a2222222-2222-4222-2222-222222222222', 'cc333333-3333-4333-3333-333333333333');
INSERT INTO public.match VALUES ('MR12', '2024-12-11 20:00:00', true, 'GROUP_STAGE', 'f9999999-9999-4999-9999-999999999999', 'f2222222-2222-4222-2222-222222222222', 13, 12, 'f9999999-9999-4999-9999-999999999999', 'a2222222-2222-4222-2222-222222222222', 'cc444444-4444-4444-4444-444444444444');
INSERT INTO public.match VALUES ('MR12', '2024-12-12 12:00:00', false, 'GROUP_STAGE', 'fbbbbbbb-bbbb-4bbb-bbbb-bbbbbbbbbbbb', 'f2222222-2222-4222-2222-222222222222', 0, 0, NULL, 'a2222222-2222-4222-2222-222222222222', 'cc555555-5555-4555-5555-555555555555');
INSERT INTO public.match VALUES ('MR12', '2024-12-12 14:00:00', false, 'GROUP_STAGE', 'f9999999-9999-4999-9999-999999999999', 'f4444444-4444-4444-4444-444444444444', 0, 0, NULL, 'a2222222-2222-4222-2222-222222222222', 'cc666666-6666-4666-6666-666666666666');
INSERT INTO public.match VALUES ('MR15', '2024-12-11 11:00:00', true, 'SEMI_FINAL', 'fccccccc-cccc-4ccc-cccc-cccccccccccc', 'f3333333-3333-4333-3333-333333333333', 12, 16, 'fccccccc-cccc-4ccc-cccc-cccccccccccc', 'a8888888-8888-4888-8888-888888888888', 'cd111111-1111-4111-1111-111111111111');
INSERT INTO public.match VALUES ('MR15', '2024-12-11 14:00:00', true, 'SEMI_FINAL', 'f6666666-6666-4666-6666-666666666666', 'f7777777-7777-4777-7777-777777777777', 16, 14, 'f5555555-5555-4555-5555-555555555555', 'a8888888-8888-4888-8888-888888888888', 'cd222222-2222-4222-2222-222222222222');
INSERT INTO public.match VALUES ('MR15', '2024-12-12 11:00:00', false, 'FINAL', 'f3333333-3333-4333-3333-333333333333', 'f6666666-6666-4666-6666-666666666666', 0, 0, NULL, 'a8888888-8888-4888-8888-888888888888', 'cd333333-3333-4333-3333-333333333333');
INSERT INTO public.match VALUES ('MR15', '2024-12-12 08:00:00', false, 'FINAL', 'f5555555-5555-4555-5555-555555555555', 'f7777777-7777-4777-7777-777777777777', 14, 8, NULL, 'a3333333-3333-4333-3333-333333333333', 'ce111111-1111-4111-1111-111111111111');
INSERT INTO public.match VALUES ('MR15', '2025-01-15 12:00:00', false, 'FINAL', 'f8888888-8888-4888-8888-888888888888', 'faaaaaaa-aaaa-4aaa-aaaa-aaaaaaaaaaaa', 0, 0, NULL, 'a9999999-9999-4999-9999-999999999999', 'cf111111-1111-4111-1111-111111111111');


--
--

INSERT INTO public.player VALUES ('BurritoBoss', 'Commander', 'Purrito', 'Mexico', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_124641_07320677.png', 19, 11, NULL, 'fbbbbbbb-bbbb-4bbb-bbbb-bbbbbbbbbbbb', 'b1c2d3e4-bbbb-4111-8111-111111111111');
INSERT INTO public.player VALUES ('TacoTiger', 'Captain', 'Tortilla', 'Spain', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_124656_9f415c2f.png', 19, 11, NULL, 'fbbbbbbb-bbbb-4bbb-bbbb-bbbbbbbbbbbb', 'b1c2d3e4-bbbb-4111-8112-111111111111');
INSERT INTO public.player VALUES ('SalsaSniper', 'Agent', 'Spicypaw', 'Chile', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_124744_f307aa76.png', 19, 11, NULL, 'fbbbbbbb-bbbb-4bbb-bbbb-bbbbbbbbbbbb', 'b1c2d3e4-bbbb-4111-8113-111111111111');
INSERT INTO public.player VALUES ('QuesoPouncer', 'Major', 'Cheeseclaw', 'Argentina', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_124759_3df60fe5.png', 19, 11, NULL, 'fbbbbbbb-bbbb-4bbb-bbbb-bbbbbbbbbbbb', 'b1c2d3e4-bbbb-4111-8114-111111111111');
INSERT INTO public.player VALUES ('GuacGuardian', 'Sergeant', 'Avocato', 'Peru', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_124819_a03980f9.png', 19, 11, NULL, 'fbbbbbbb-bbbb-4bbb-bbbb-bbbbbbbbbbbb', 'b1c2d3e4-bbbb-4111-8115-111111111111');
INSERT INTO public.player VALUES ('WarriorWhisker', 'Commander', 'Whiskerton', 'UK', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_124846_398d141e.png', 20, 12, NULL, 'f2222222-2222-4222-2222-222222222222', 'b2222222-2222-4222-2222-222222222221');
INSERT INTO public.player VALUES ('StrikeFury', 'Captain', 'Furington', 'Canada', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_125124_f83eaf9a.png', 18, 8, NULL, 'f3333333-3333-4333-3333-333333333333', 'b3333333-3333-4333-3333-333333333334');
INSERT INTO public.player VALUES ('NipNinja', 'Master', 'Nipjai', 'Japan', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_125136_395f04ce.png', 18, 8, NULL, 'f3333333-3333-4333-3333-333333333333', 'b3333333-3333-4333-3333-333333333335');
INSERT INTO public.player VALUES ('CatnipSniper', 'Elite', 'Snipurr', 'Germany', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_125150_e456392f.png', 18, 8, NULL, 'f3333333-3333-4333-3333-333333333333', 'b3333333-3333-4333-3333-333333333336');
INSERT INTO public.player VALUES ('NipStalker', 'Agent', 'Stalkerton', 'Russia', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_125224_191beaef.png', 18, 8, NULL, 'f3333333-3333-4333-3333-333333333333', 'b3333333-3333-4333-3333-333333333337');
INSERT INTO public.player VALUES ('MayhemMittens', 'Chaos', 'Mittensworth', 'USA', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_125247_fc379774.png', 15, 7, NULL, 'f4444444-4444-4444-4444-444444444444', 'b4444444-4444-4444-4444-444444444441');
INSERT INTO public.player VALUES ('MittenMaster', 'Lord', 'Mittenton', 'UK', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_125316_50b9d3fa.png', 15, 7, NULL, 'f4444444-4444-4444-4444-444444444444', 'b4444444-4444-4444-4444-444444444442');
INSERT INTO public.player VALUES ('ChaosPaw', 'Agent', 'Pawsworth', 'Canada', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_125413_d9ac5b00.png', 15, 7, NULL, 'f4444444-4444-4444-4444-444444444444', 'b4444444-4444-4444-4444-444444444443');
INSERT INTO public.player VALUES ('MittenMerc', 'Captain', 'Mercenary', 'Australia', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_125449_d2416e61.png', 15, 7, NULL, 'f4444444-4444-4444-4444-444444444444', 'b4444444-4444-4444-4444-444444444444');
INSERT INTO public.player VALUES ('StrikeMitten', 'Commander', 'Strikeworth', 'Germany', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_125504_808025dd.png', 15, 7, NULL, 'f4444444-4444-4444-4444-444444444444', 'b4444444-4444-4444-4444-444444444445');
INSERT INTO public.player VALUES ('ElitePaw', 'Supreme', 'Pawlite', 'USA', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_125519_164abf8a.png', 12, 6, NULL, 'f5555555-5555-4555-5555-555555555555', 'b5555555-5555-4555-5555-555555555551');
INSERT INTO public.player VALUES ('PatrolPrime', 'Elite', 'Primepaw', 'UK', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_125538_8593cd1e.png', 12, 6, NULL, 'f5555555-5555-4555-5555-555555555555', 'b5555555-5555-4555-5555-555555555552');
INSERT INTO public.player VALUES ('GuardianPaw', 'Sentinel', 'Guardpaw', 'Canada', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_125556_097384f6.png', 12, 6, NULL, 'f5555555-5555-4555-5555-555555555555', 'b5555555-5555-4555-5555-555555555553');
INSERT INTO public.player VALUES ('PawForce', 'Commander', 'Forceworth', 'France', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_125608_b848f99e.png', 12, 6, NULL, 'f5555555-5555-4555-5555-555555555555', 'b5555555-5555-4555-5555-555555555554');
INSERT INTO public.player VALUES ('EliteStrike', 'Captain', 'Strikepaw', 'Germany', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_125623_74662d8e.png', 12, 6, NULL, 'f5555555-5555-4555-5555-555555555555', 'b5555555-5555-4555-5555-555555555555');
INSERT INTO public.player VALUES ('MercMeow', 'Captain', 'Mercworth', 'USA', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_125909_467ea824.png', 8, 3, NULL, 'f7777777-7777-4777-7777-777777777777', 'b7777777-7777-4777-7777-777777777771');
INSERT INTO public.player VALUES ('MeowMerc', 'Commander', 'Mercaton', 'UK', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_125922_603ea037.png', 8, 3, NULL, 'f7777777-7777-4777-7777-777777777777', 'b7777777-7777-4777-7777-777777777772');
INSERT INTO public.player VALUES ('MercMaster', 'Major', 'Mastermerc', 'Russia', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_125949_773fcc96.png', 8, 3, NULL, 'f7777777-7777-4777-7777-777777777777', 'b7777777-7777-4777-7777-777777777773');
INSERT INTO public.player VALUES ('StrikeMerc', 'Lieutenant', 'Strikeworth', 'Germany', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_130003_546b2749.png', 8, 3, NULL, 'f7777777-7777-4777-7777-777777777777', 'b7777777-7777-4777-7777-777777777774');
INSERT INTO public.player VALUES ('MercNinja', 'Shadow', 'Ninjamerc', 'Japan', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_130017_e239043a.png', 8, 3, NULL, 'f7777777-7777-4777-7777-777777777777', 'b7777777-7777-4777-7777-777777777775');
INSERT INTO public.player VALUES ('MercPaw', 'Agent', 'Pawmerc', 'France', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241125_195908_e14b3ecf.png', 8, 3, NULL, 'f7777777-7777-4777-7777-777777777777', 'b7777777-7777-4777-7777-777777777776');
INSERT INTO public.player VALUES ('EliteMerc', 'Elite', 'Mercton', 'Spain', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241125_200817_2529533c.png', 8, 3, NULL, 'f7777777-7777-4777-7777-777777777777', 'b7777777-7777-4777-7777-777777777777');
INSERT INTO public.player VALUES ('ScratchLord', 'Admiral', 'Scratchington', 'USA', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241125_203217_874d1a25.png', 22, 15, NULL, 'f8888888-8888-4888-8888-888888888888', 'b8888888-8888-4888-8888-888888888881');
INSERT INTO public.player VALUES ('SquadScratch', 'Wing', 'Commander', 'UK', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_123123_5ca24ab3.png', 22, 15, NULL, 'f8888888-8888-4888-8888-888888888888', 'b8888888-8888-4888-8888-888888888882');
INSERT INTO public.player VALUES ('AceScratch', 'Flight', 'Lieutenant', 'Canada', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_123145_3fb30411.png', 22, 15, NULL, 'f8888888-8888-4888-8888-888888888888', 'b8888888-8888-4888-8888-888888888883');
INSERT INTO public.player VALUES ('ScratchPilot', 'Captain', 'Skyworth', 'Australia', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_124514_d9b7b50a.png', 22, 15, NULL, 'f8888888-8888-4888-8888-888888888888', 'b8888888-8888-4888-8888-888888888884');
INSERT INTO public.player VALUES ('RainbowRogue', 'Master', 'Nyaninja', 'Japan', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_124530_bb2ab86f.png', 13, 5, NULL, 'fccccccc-cccc-4ccc-cccc-cccccccccccc', 'c1d2e3f4-cccc-4111-8111-111111111111');
INSERT INTO public.player VALUES ('SneakyPaw', 'Ninja', 'Pawsome', 'Japan', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241125_195908_e14b3ecf.png', 10, 4, NULL, 'f1111111-1111-4111-1111-111111111111', 'a1b2c3d4-1111-4111-1111-111111111111');
INSERT INTO public.player VALUES ('FuryClaws', 'Captain', 'Scratch', 'USA', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241125_200817_2529533c.png', 10, 4, NULL, 'f1111111-1111-4111-1111-111111111111', 'a1b2c3d4-1111-4111-1111-111111111112');
INSERT INTO public.player VALUES ('WhiskerBlade', 'Shadow', 'Whiskers', 'Russia', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241125_203217_874d1a25.png', 10, 4, NULL, 'f1111111-1111-4111-1111-111111111111', 'a1b2c3d4-1111-4111-1111-111111111113');
INSERT INTO public.player VALUES ('NightStalker', 'Silent', 'Hunter', 'Germany', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_123123_5ca24ab3.png', 10, 4, NULL, 'f1111111-1111-4111-1111-111111111111', 'a1b2c3d4-1111-4111-1111-111111111114');
INSERT INTO public.player VALUES ('ScorpionScratch', 'Master', 'Clawality', 'Japan', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_123145_3fb30411.png', 16, 9, NULL, 'faaaaaaa-aaaa-4aaa-aaaa-aaaaaaaaaaaa', 'a1b2c3d4-aaaa-4111-8111-111111111111');
INSERT INTO public.player VALUES ('SubZeroPurr', 'Lord', 'Freezepaw', 'China', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_124514_d9b7b50a.png', 16, 9, NULL, 'faaaaaaa-aaaa-4aaa-aaaa-aaaaaaaaaaaa', 'a1b2c3d4-aaaa-4111-8112-111111111111');
INSERT INTO public.player VALUES ('RaidenWhiskers', 'Thunder', 'Stormclaw', 'USA', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_124530_bb2ab86f.png', 16, 9, NULL, 'faaaaaaa-aaaa-4aaa-aaaa-aaaaaaaaaaaa', 'a1b2c3d4-aaaa-4111-8113-111111111111');
INSERT INTO public.player VALUES ('KittyKahn', 'Emperor', 'Soulcatcher', 'Mongolia', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_124544_4e0eb30b.png', 16, 9, NULL, 'faaaaaaa-aaaa-4aaa-aaaa-aaaaaaaaaaaa', 'a1b2c3d4-aaaa-4111-8114-111111111111');
INSERT INTO public.player VALUES ('JaxPaws', 'Major', 'Steelclaws', 'UK', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_124625_5f140174.png', 16, 9, NULL, 'faaaaaaa-aaaa-4aaa-aaaa-aaaaaaaaaaaa', 'a1b2c3d4-aaaa-4111-8115-111111111111');
INSERT INTO public.player VALUES ('StealthPurr', 'Ghost', 'Purrington', 'Canada', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_124900_31df2c18.png', 20, 12, NULL, 'f2222222-2222-4222-2222-222222222222', 'b2222222-2222-4222-2222-222222222222');
INSERT INTO public.player VALUES ('TacticalMeow', 'Sergeant', 'Meowster', 'France', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_124938_09d33e01.png', 20, 12, NULL, 'f2222222-2222-4222-2222-222222222222', 'b2222222-2222-4222-2222-222222222223');
INSERT INTO public.player VALUES ('ShadowClaw', 'Agent', 'Clawford', 'Spain', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_124954_d44ebf2e.png', 20, 12, NULL, 'f2222222-2222-4222-2222-222222222222', 'b2222222-2222-4222-2222-222222222224');
INSERT INTO public.player VALUES ('WhiskerSnipe', 'Major', 'Snipurr', 'Italy', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_125008_3859f407.png', 20, 12, NULL, 'f2222222-2222-4222-2222-222222222222', 'b2222222-2222-4222-2222-222222222225');
INSERT INTO public.player VALUES ('NinjaKitten', 'Shadow', 'Kittenshi', 'Japan', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_125024_9468085c.png', 20, 12, NULL, 'f2222222-2222-4222-2222-222222222222', 'b2222222-2222-4222-2222-222222222226');
INSERT INTO public.player VALUES ('CatnipKing', 'Lord', 'Catnipston', 'USA', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_125039_ad82155f.png', 18, 8, NULL, 'f3333333-3333-4333-3333-333333333333', 'b3333333-3333-4333-3333-333333333331');
INSERT INTO public.player VALUES ('NipHunter', 'Duke', 'Nipsworth', 'UK', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_125056_2450e2c5.png', 18, 8, NULL, 'f3333333-3333-4333-3333-333333333333', 'b3333333-3333-4333-3333-333333333332');
INSERT INTO public.player VALUES ('CommandoPurr', 'General', 'Purrton', 'Australia', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_125110_6d792842.png', 18, 8, NULL, 'f3333333-3333-4333-3333-333333333333', 'b3333333-3333-4333-3333-333333333333');
INSERT INTO public.player VALUES ('PatrolSniper', 'Agent', 'Snipaw', 'Russia', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_125642_97657080.png', 12, 6, NULL, 'f5555555-5555-4555-5555-555555555555', 'b5555555-5555-4555-5555-555555555556');
INSERT INTO public.player VALUES ('GuardMaster', 'Master', 'Guardton', 'Spain', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_125656_f097c811.png', 12, 6, NULL, 'f5555555-5555-4555-5555-555555555555', 'b5555555-5555-4555-5555-555555555557');
INSERT INTO public.player VALUES ('EliteNinja', 'Shadow', 'Ninjpaw', 'Japan', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_125712_5ed6942d.png', 12, 6, NULL, 'f5555555-5555-4555-5555-555555555555', 'b5555555-5555-4555-5555-555555555558');
INSERT INTO public.player VALUES ('ProPurr', 'Legend', 'Purrfect', 'USA', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_125732_cc1190b6.png', 25, 18, NULL, 'f6666666-6666-4666-6666-666666666666', 'b6666666-6666-4666-6666-666666666661');
INSERT INTO public.player VALUES ('AcePurr', 'Master', 'Aceworth', 'UK', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_125751_400acb77.png', 25, 18, NULL, 'f6666666-6666-4666-6666-666666666666', 'b6666666-6666-4666-6666-666666666662');
INSERT INTO public.player VALUES ('PurrPro', 'Elite', 'Proton', 'Canada', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_125805_6e95cefa.png', 25, 18, NULL, 'f6666666-6666-4666-6666-666666666666', 'b6666666-6666-4666-6666-666666666663');
INSERT INTO public.player VALUES ('ProMeow', 'Champion', 'Meowster', 'France', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_125818_388d7e45.png', 25, 18, NULL, 'f6666666-6666-4666-6666-666666666666', 'b6666666-6666-4666-6666-666666666664');
INSERT INTO public.player VALUES ('PurrMaster', 'Grandmaster', 'Masterworth', 'Germany', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_125832_64daa280.png', 25, 18, NULL, 'f6666666-6666-4666-6666-666666666666', 'b6666666-6666-4666-6666-666666666665');
INSERT INTO public.player VALUES ('ProStrike', 'Supreme', 'Striker', 'Japan', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_125856_00d3fd81.png', 25, 18, NULL, 'f6666666-6666-4666-6666-666666666666', 'b6666666-6666-4666-6666-666666666666');
INSERT INTO public.player VALUES ('ProMomo', 'Momo', 'Momos', 'Bulgaria', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_124530_bb2ab86f.png', 0, 0, NULL, NULL, 'b8888888-8888-4888-8888-888888888885');
INSERT INTO public.player VALUES ('PixelProwler', 'Shadow', 'Byteclaw', 'South Korea', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_124544_4e0eb30b.png', 13, 5, NULL, 'fccccccc-cccc-4ccc-cccc-cccccccccccc', 'c1d2e3f4-cccc-4111-8112-111111111111');
INSERT INTO public.player VALUES ('MemeMaster', 'Agent', 'Lolcat', 'Taiwan', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_124625_5f140174.png', 13, 5, NULL, 'fccccccc-cccc-4ccc-cccc-cccccccccccc', 'c1d2e3f4-cccc-4111-8113-111111111111');
INSERT INTO public.player VALUES ('PopTartPouncer', 'Ninja', 'Rainbowpaw', 'Singapore', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_124641_07320677.png', 13, 5, NULL, 'fccccccc-cccc-4ccc-cccc-cccccccccccc', 'c1d2e3f4-cccc-4111-8114-111111111111');
INSERT INTO public.player VALUES ('StardustStalker', 'Captain', 'Spacepaw', 'Hong Kong', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_124656_9f415c2f.png', 13, 5, NULL, 'fccccccc-cccc-4ccc-cccc-cccccccccccc', 'c1d2e3f4-cccc-4111-8115-111111111111');
INSERT INTO public.player VALUES ('YarnYolo', 'Supreme', 'Thrower', 'USA', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_124744_f307aa76.png', 14, 6, NULL, 'f9999999-9999-4999-9999-999999999999', 'd1e2f3a4-9999-4111-8111-111111111111');
INSERT INTO public.player VALUES ('StringSlinger', 'Captain', 'Woolsworth', 'Canada', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_124759_3df60fe5.png', 14, 6, NULL, 'f9999999-9999-4999-9999-999999999999', 'd1e2f3a4-9999-4111-8112-111111111111');
INSERT INTO public.player VALUES ('KnitNinja', 'Agent', 'Threadripper', 'UK', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_124819_a03980f9.png', 14, 6, NULL, 'f9999999-9999-4999-9999-999999999999', 'd1e2f3a4-9999-4111-8113-111111111111');
INSERT INTO public.player VALUES ('WoolWarrior', 'Commander', 'Yeetmaster', 'Australia', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_124846_398d141e.png', 14, 6, NULL, 'f9999999-9999-4999-9999-999999999999', 'd1e2f3a4-9999-4111-8114-111111111111');
INSERT INTO public.player VALUES ('Ballistic_Ball', 'Private', 'Stringshot', 'New Zealand', 'https://kittenstrike.s3.eu-north-1.amazonaws.com/players/20241127_124900_31df2c18.png', 14, 6, NULL, 'f9999999-9999-4999-9999-999999999999', 'd1e2f3a4-9999-4111-8115-111111111111');


--
--

INSERT INTO public.prizecut VALUES (1, 7000, 'a1111111-1111-4111-1111-111111111111', 'f1111111-1111-4111-1111-111111111111', 'ec111111-1111-4111-1111-111111111111');
INSERT INTO public.prizecut VALUES (2, 3000, 'a1111111-1111-4111-1111-111111111111', 'f6666666-6666-4666-6666-666666666666', 'ec222222-2222-4222-2222-222222222222');
INSERT INTO public.prizecut VALUES (1, 8400, 'a4444444-4444-4444-4444-444444444444', 'f2222222-2222-4222-2222-222222222222', 'ec777777-7777-4777-7777-777777777777');
INSERT INTO public.prizecut VALUES (2, 3600, 'a4444444-4444-4444-4444-444444444444', 'f7777777-7777-4777-7777-777777777777', 'ec888888-8888-4888-8888-888888888888');
INSERT INTO public.prizecut VALUES (1, 5600, 'a5555555-5555-4555-5555-555555555555', 'f8888888-8888-4888-8888-888888888888', 'ec333333-3333-4333-3333-333333333333');
INSERT INTO public.prizecut VALUES (2, 2400, 'a5555555-5555-4555-5555-555555555555', 'f4444444-4444-4444-4444-444444444444', 'ec444444-4444-4444-4444-444444444444');
INSERT INTO public.prizecut VALUES (1, 10500, 'a6666666-6666-4666-6666-666666666666', 'f8888888-8888-4888-8888-888888888888', 'ec999999-9999-4999-9999-999999999999');
INSERT INTO public.prizecut VALUES (2, 4500, 'a6666666-6666-4666-6666-666666666666', 'f1111111-1111-4111-1111-111111111111', 'ecaaaaaa-aaaa-4aaa-aaaa-aaaaaaaaaaaa');
INSERT INTO public.prizecut VALUES (1, 12600, 'a7777777-7777-4777-7777-777777777777', 'f6666666-6666-4666-6666-666666666666', 'ec555555-5555-4555-5555-555555555555');
INSERT INTO public.prizecut VALUES (2, 5400, 'a7777777-7777-4777-7777-777777777777', 'fbbbbbbb-bbbb-4bbb-bbbb-bbbbbbbbbbbb', 'ec666666-6666-4666-6666-666666666666');
INSERT INTO public.prizecut VALUES (1, 10500, 'a2222222-2222-4222-2222-222222222222', NULL, 'ecbbbbbb-bbbb-4bbb-bbbb-bbbbbbbbbbbb');
INSERT INTO public.prizecut VALUES (2, 4500, 'a2222222-2222-4222-2222-222222222222', NULL, 'eccccccc-cccc-4ccc-cccc-cccccccccccc');
INSERT INTO public.prizecut VALUES (1, 9100, 'a8888888-8888-4888-8888-888888888888', NULL, 'ecdddddd-dddd-4ddd-dddd-dddddddddddd');
INSERT INTO public.prizecut VALUES (2, 3900, 'a8888888-8888-4888-8888-888888888888', NULL, 'eceeeeee-eeee-4eee-eeee-eeeeeeeeeeee');
INSERT INTO public.prizecut VALUES (1, 14000, 'a3333333-3333-4333-3333-333333333333', NULL, 'ecffffff-ffff-4fff-ffff-ffffffffffff');
INSERT INTO public.prizecut VALUES (2, 6000, 'a3333333-3333-4333-3333-333333333333', NULL, 'ecaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa');
INSERT INTO public.prizecut VALUES (1, 11200, 'a9999999-9999-4999-9999-999999999999', NULL, 'ec222222-aaaa-4bbb-8ccc-dddddddddddd');
INSERT INTO public.prizecut VALUES (2, 4800, 'a9999999-9999-4999-9999-999999999999', NULL, 'ec111111-2222-4333-8444-555555555555');


--
--

INSERT INTO public.request VALUES ('PENDING', '2024-11-08 10:00:00+02', NULL, 'PROMOTE_USER_TO_DIRECTOR', 'e3333333-3333-4333-3333-333333333333', NULL, NULL, 'd1111111-1111-4111-1111-111111111111');
INSERT INTO public.request VALUES ('PENDING', '2024-11-07 15:30:00+02', NULL, 'PROMOTE_USER_TO_DIRECTOR', 'e3333333-3333-4333-3333-333333333333', NULL, NULL, 'd2222222-2222-4222-2222-222222222222');
INSERT INTO public.request VALUES ('PENDING', '2024-11-08 09:15:00+02', NULL, 'PROMOTE_USER_TO_DIRECTOR', 'e4444444-4444-4444-4444-444444444444', NULL, NULL, 'd3333333-3333-4333-3333-333333333333');
INSERT INTO public.request VALUES ('PENDING', '2024-11-08 11:30:00+02', NULL, 'PROMOTE_USER_TO_DIRECTOR', 'e5555555-5555-4555-5555-555555555555', NULL, NULL, 'd4444444-4444-4444-4444-444444444444');
INSERT INTO public.request VALUES ('PENDING', '2024-11-08 14:45:00+02', NULL, 'PROMOTE_USER_TO_DIRECTOR', 'e6666666-6666-4666-6666-666666666666', NULL, NULL, 'd5555555-5555-4555-5555-555555555555');
INSERT INTO public.request VALUES ('PENDING', '2024-11-08 16:20:00+02', NULL, 'PROMOTE_USER_TO_DIRECTOR', 'e7777777-7777-4777-7777-777777777777', NULL, NULL, 'd6666666-6666-4666-6666-666666666666');
INSERT INTO public.request VALUES ('PENDING', '2024-11-08 17:00:00+02', NULL, 'PROMOTE_USER_TO_DIRECTOR', 'e8888888-8888-4888-8888-888888888888', NULL, NULL, 'd7777777-7777-4777-7777-777777777777');


--
-- PostgreSQL database dump complete
--

