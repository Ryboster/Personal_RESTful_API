--
-- PostgreSQL database dump
--

\restrict j31b72Gcs2zjjg8V4GljhfvzZ5GUfL5NvycFhnc9UHQNaEucbFBmW0qDNXdq9FU

-- Dumped from database version 14.19 (Ubuntu 14.19-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.19 (Ubuntu 14.19-0ubuntu0.22.04.1)

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: collaborations; Type: TABLE; Schema: public; Owner: guest
--

CREATE TABLE public.collaborations (
    collaboration_id integer NOT NULL,
    name text NOT NULL,
    description text NOT NULL,
    content text
);


ALTER TABLE public.collaborations OWNER TO guest;

--
-- Name: collaborations_collaboration_id_seq; Type: SEQUENCE; Schema: public; Owner: guest
--

CREATE SEQUENCE public.collaborations_collaboration_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.collaborations_collaboration_id_seq OWNER TO guest;

--
-- Name: collaborations_collaboration_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: guest
--

ALTER SEQUENCE public.collaborations_collaboration_id_seq OWNED BY public.collaborations.collaboration_id;


--
-- Name: collaborators; Type: TABLE; Schema: public; Owner: guest
--

CREATE TABLE public.collaborators (
    collaborator_id integer NOT NULL,
    name text NOT NULL,
    role text NOT NULL,
    social_url text
);


ALTER TABLE public.collaborators OWNER TO guest;

--
-- Name: collaborators_collaborator_id_seq; Type: SEQUENCE; Schema: public; Owner: guest
--

CREATE SEQUENCE public.collaborators_collaborator_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.collaborators_collaborator_id_seq OWNER TO guest;

--
-- Name: collaborators_collaborator_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: guest
--

ALTER SEQUENCE public.collaborators_collaborator_id_seq OWNED BY public.collaborators.collaborator_id;


--
-- Name: collabs_join; Type: TABLE; Schema: public; Owner: guest
--

CREATE TABLE public.collabs_join (
    collaboration_id integer,
    collaborator_id integer
);


ALTER TABLE public.collabs_join OWNER TO guest;

--
-- Name: feedbacks; Type: TABLE; Schema: public; Owner: guest
--

CREATE TABLE public.feedbacks (
    feedback_id integer NOT NULL,
    author text NOT NULL,
    feedback text NOT NULL
);


ALTER TABLE public.feedbacks OWNER TO guest;

--
-- Name: feedbacks_feedback_id_seq; Type: SEQUENCE; Schema: public; Owner: guest
--

CREATE SEQUENCE public.feedbacks_feedback_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.feedbacks_feedback_id_seq OWNER TO guest;

--
-- Name: feedbacks_feedback_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: guest
--

ALTER SEQUENCE public.feedbacks_feedback_id_seq OWNED BY public.feedbacks.feedback_id;


--
-- Name: projects; Type: TABLE; Schema: public; Owner: guest
--

CREATE TABLE public.projects (
    project_id integer NOT NULL,
    name text NOT NULL,
    description text NOT NULL,
    content text
);


ALTER TABLE public.projects OWNER TO guest;

--
-- Name: projects_project_id_seq; Type: SEQUENCE; Schema: public; Owner: guest
--

CREATE SEQUENCE public.projects_project_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.projects_project_id_seq OWNER TO guest;

--
-- Name: projects_project_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: guest
--

ALTER SEQUENCE public.projects_project_id_seq OWNED BY public.projects.project_id;


--
-- Name: sessions; Type: TABLE; Schema: public; Owner: guest
--

CREATE TABLE public.sessions (
    user_id integer NOT NULL,
    token text NOT NULL,
    expiry integer NOT NULL
);


ALTER TABLE public.sessions OWNER TO guest;

--
-- Name: submissions; Type: TABLE; Schema: public; Owner: guest
--

CREATE TABLE public.submissions (
    submission_id integer NOT NULL,
    source text NOT NULL,
    fact text NOT NULL,
    co2 real NOT NULL,
    timespan integer NOT NULL
);


ALTER TABLE public.submissions OWNER TO guest;

--
-- Name: submissions_submission_id_seq; Type: SEQUENCE; Schema: public; Owner: guest
--

CREATE SEQUENCE public.submissions_submission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.submissions_submission_id_seq OWNER TO guest;

--
-- Name: submissions_submission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: guest
--

ALTER SEQUENCE public.submissions_submission_id_seq OWNED BY public.submissions.submission_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: guest
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    email text NOT NULL,
    isadmin boolean NOT NULL,
    username text NOT NULL,
    password text NOT NULL
);


ALTER TABLE public.users OWNER TO guest;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: guest
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_user_id_seq OWNER TO guest;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: guest
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: collaborations collaboration_id; Type: DEFAULT; Schema: public; Owner: guest
--

ALTER TABLE ONLY public.collaborations ALTER COLUMN collaboration_id SET DEFAULT nextval('public.collaborations_collaboration_id_seq'::regclass);


--
-- Name: collaborators collaborator_id; Type: DEFAULT; Schema: public; Owner: guest
--

ALTER TABLE ONLY public.collaborators ALTER COLUMN collaborator_id SET DEFAULT nextval('public.collaborators_collaborator_id_seq'::regclass);


--
-- Name: feedbacks feedback_id; Type: DEFAULT; Schema: public; Owner: guest
--

ALTER TABLE ONLY public.feedbacks ALTER COLUMN feedback_id SET DEFAULT nextval('public.feedbacks_feedback_id_seq'::regclass);


--
-- Name: projects project_id; Type: DEFAULT; Schema: public; Owner: guest
--

ALTER TABLE ONLY public.projects ALTER COLUMN project_id SET DEFAULT nextval('public.projects_project_id_seq'::regclass);


--
-- Name: submissions submission_id; Type: DEFAULT; Schema: public; Owner: guest
--

ALTER TABLE ONLY public.submissions ALTER COLUMN submission_id SET DEFAULT nextval('public.submissions_submission_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: guest
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Data for Name: collaborations; Type: TABLE DATA; Schema: public; Owner: guest
--

COPY public.collaborations (collaboration_id, name, description, content) FROM stdin;
1	x	 x	\N
4	kbhgi	 tyjhjgh	\N
\.


--
-- Data for Name: collaborators; Type: TABLE DATA; Schema: public; Owner: guest
--

COPY public.collaborators (collaborator_id, name, role, social_url) FROM stdin;
\.


--
-- Data for Name: collabs_join; Type: TABLE DATA; Schema: public; Owner: guest
--

COPY public.collabs_join (collaboration_id, collaborator_id) FROM stdin;
\.


--
-- Data for Name: feedbacks; Type: TABLE DATA; Schema: public; Owner: guest
--

COPY public.feedbacks (feedback_id, author, feedback) FROM stdin;
\.


--
-- Data for Name: projects; Type: TABLE DATA; Schema: public; Owner: guest
--

COPY public.projects (project_id, name, description, content) FROM stdin;
\.


--
-- Data for Name: sessions; Type: TABLE DATA; Schema: public; Owner: guest
--

COPY public.sessions (user_id, token, expiry) FROM stdin;
1	72b6c2927bdbeb9186dc4539d851962813cdf19e456a143017a0c2df42263792	1761767095
1	203c1fe67b6c082781963ee960422b33c4f1a2a10f9b2d96534bb397aff3898c	1761811949
1	0118ad13277b8bebe0407f0383199629588bdc48883cbb34e2dbb9903f3c9d19	1761814999
1	abc6dd65e4dc2aedf762f73c9c5ec5bf121762afde673265eef192a5892e8f35	1761818753
1	efca9cf6f8680a85f508d481520603fd3115b677d0bfdab938b00b3717937c86	1761820584
\.


--
-- Data for Name: submissions; Type: TABLE DATA; Schema: public; Owner: guest
--

COPY public.submissions (submission_id, source, fact, co2, timespan) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: guest
--

COPY public.users (user_id, email, isadmin, username, password) FROM stdin;
1	gracjanblazejowski1@gmail.com	t	Snekster1	X120ppZZ((0..zzA
\.


--
-- Name: collaborations_collaboration_id_seq; Type: SEQUENCE SET; Schema: public; Owner: guest
--

SELECT pg_catalog.setval('public.collaborations_collaboration_id_seq', 4, true);


--
-- Name: collaborators_collaborator_id_seq; Type: SEQUENCE SET; Schema: public; Owner: guest
--

SELECT pg_catalog.setval('public.collaborators_collaborator_id_seq', 1, false);


--
-- Name: feedbacks_feedback_id_seq; Type: SEQUENCE SET; Schema: public; Owner: guest
--

SELECT pg_catalog.setval('public.feedbacks_feedback_id_seq', 1, true);


--
-- Name: projects_project_id_seq; Type: SEQUENCE SET; Schema: public; Owner: guest
--

SELECT pg_catalog.setval('public.projects_project_id_seq', 9, true);


--
-- Name: submissions_submission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: guest
--

SELECT pg_catalog.setval('public.submissions_submission_id_seq', 1, false);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: guest
--

SELECT pg_catalog.setval('public.users_user_id_seq', 1, true);


--
-- Name: collaborations collaborations_description_key; Type: CONSTRAINT; Schema: public; Owner: guest
--

ALTER TABLE ONLY public.collaborations
    ADD CONSTRAINT collaborations_description_key UNIQUE (description);


--
-- Name: collaborations collaborations_name_key; Type: CONSTRAINT; Schema: public; Owner: guest
--

ALTER TABLE ONLY public.collaborations
    ADD CONSTRAINT collaborations_name_key UNIQUE (name);


--
-- Name: collaborations collaborations_pkey; Type: CONSTRAINT; Schema: public; Owner: guest
--

ALTER TABLE ONLY public.collaborations
    ADD CONSTRAINT collaborations_pkey PRIMARY KEY (collaboration_id);


--
-- Name: collaborators collaborators_name_key; Type: CONSTRAINT; Schema: public; Owner: guest
--

ALTER TABLE ONLY public.collaborators
    ADD CONSTRAINT collaborators_name_key UNIQUE (name);


--
-- Name: collaborators collaborators_pkey; Type: CONSTRAINT; Schema: public; Owner: guest
--

ALTER TABLE ONLY public.collaborators
    ADD CONSTRAINT collaborators_pkey PRIMARY KEY (collaborator_id);


--
-- Name: collaborators collaborators_role_key; Type: CONSTRAINT; Schema: public; Owner: guest
--

ALTER TABLE ONLY public.collaborators
    ADD CONSTRAINT collaborators_role_key UNIQUE (role);


--
-- Name: feedbacks feedbacks_pkey; Type: CONSTRAINT; Schema: public; Owner: guest
--

ALTER TABLE ONLY public.feedbacks
    ADD CONSTRAINT feedbacks_pkey PRIMARY KEY (feedback_id);


--
-- Name: projects projects_pkey; Type: CONSTRAINT; Schema: public; Owner: guest
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_pkey PRIMARY KEY (project_id);


--
-- Name: sessions sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: guest
--

ALTER TABLE ONLY public.sessions
    ADD CONSTRAINT sessions_pkey PRIMARY KEY (token);


--
-- Name: submissions submissions_fact_key; Type: CONSTRAINT; Schema: public; Owner: guest
--

ALTER TABLE ONLY public.submissions
    ADD CONSTRAINT submissions_fact_key UNIQUE (fact);


--
-- Name: submissions submissions_pkey; Type: CONSTRAINT; Schema: public; Owner: guest
--

ALTER TABLE ONLY public.submissions
    ADD CONSTRAINT submissions_pkey PRIMARY KEY (submission_id);


--
-- Name: submissions submissions_source_key; Type: CONSTRAINT; Schema: public; Owner: guest
--

ALTER TABLE ONLY public.submissions
    ADD CONSTRAINT submissions_source_key UNIQUE (source);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: guest
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: guest
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: guest
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: collabs_join collabs_join_collaboration_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: guest
--

ALTER TABLE ONLY public.collabs_join
    ADD CONSTRAINT collabs_join_collaboration_id_fkey FOREIGN KEY (collaboration_id) REFERENCES public.collaborations(collaboration_id) ON DELETE CASCADE;


--
-- Name: collabs_join collabs_join_collaborator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: guest
--

ALTER TABLE ONLY public.collabs_join
    ADD CONSTRAINT collabs_join_collaborator_id_fkey FOREIGN KEY (collaborator_id) REFERENCES public.collaborators(collaborator_id);


--
-- Name: sessions sessions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: guest
--

ALTER TABLE ONLY public.sessions
    ADD CONSTRAINT sessions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict j31b72Gcs2zjjg8V4GljhfvzZ5GUfL5NvycFhnc9UHQNaEucbFBmW0qDNXdq9FU

