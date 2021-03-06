PGDMP                     
    y            DashboardLookatMe    13.2    13.2 J    1           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            2           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            3           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            4           1262    17520    DashboardLookatMe    DATABASE     s   CREATE DATABASE "DashboardLookatMe" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'English_Indonesia.1252';
 #   DROP DATABASE "DashboardLookatMe";
                postgres    false            5           0    0    DATABASE "DashboardLookatMe"    COMMENT     7   COMMENT ON DATABASE "DashboardLookatMe" IS 'Database';
                   postgres    false    3124            ?           1247    17657    status_t    TYPE     L   CREATE TYPE public.status_t AS ENUM (
    'Available',
    'Unavailable'
);
    DROP TYPE public.status_t;
       public          postgres    false            ?           1247    17533    valid_gender    TYPE     n   CREATE TYPE public.valid_gender AS ENUM (
    'Laki-laki',
    'Perempuan',
    'Prefer tidak menyebutkan'
);
    DROP TYPE public.valid_gender;
       public          postgres    false            ?           1247    17558    valid_jabatan    TYPE     q   CREATE TYPE public.valid_jabatan AS ENUM (
    'Admin',
    'CEO',
    'CMO',
    'CFO',
    'CTO',
    'COO'
);
     DROP TYPE public.valid_jabatan;
       public          postgres    false            ?           1247    17581    valid_kategori    TYPE     w   CREATE TYPE public.valid_kategori AS ENUM (
    'Atasan',
    'Bawahan',
    'Outer',
    'Masker',
    'Aksesoris'
);
 !   DROP TYPE public.valid_kategori;
       public          postgres    false            ?           1247    17695    valid_status    TYPE     ^   CREATE TYPE public.valid_status AS ENUM (
    'Terima',
    'Tolak',
    'Belum disetujui'
);
    DROP TYPE public.valid_status;
       public          postgres    false            ?            1255    17749    isiidresponden()    FUNCTION     ?   CREATE FUNCTION public.isiidresponden() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
	INSERT INTO responden(idResponden)
		 VALUES(NEW.idCust);
	RETURN NEW;
END;
$$;
 '   DROP FUNCTION public.isiidresponden();
       public          postgres    false            ?            1255    17752    isiidrespondenadmin()    FUNCTION     ?   CREATE FUNCTION public.isiidrespondenadmin() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
	INSERT INTO responden(idResponden)
		 VALUES(NEW.idAdm);
	RETURN NEW;
END;
$$;
 ,   DROP FUNCTION public.isiidrespondenadmin();
       public          postgres    false            ?            1259    17767    admin    TABLE       CREATE TABLE public.admin (
    idadm character(8) NOT NULL,
    nama character varying(30) NOT NULL,
    username character varying NOT NULL,
    password character varying NOT NULL,
    jabatan public.valid_jabatan NOT NULL,
    jobdesc text,
    notelp character(13) NOT NULL
);
    DROP TABLE public.admin;
       public         heap    postgres    false    646            ?            1259    17754    admin_id_seq    SEQUENCE     u   CREATE SEQUENCE public.admin_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.admin_id_seq;
       public          postgres    false    217            6           0    0    admin_id_seq    SEQUENCE OWNED BY     @   ALTER SEQUENCE public.admin_id_seq OWNED BY public.admin.idadm;
          public          postgres    false    214            ?            1259    17758    customer    TABLE     <  CREATE TABLE public.customer (
    idcust character(8) NOT NULL,
    namacust character varying(30) NOT NULL,
    username character varying NOT NULL,
    password character varying NOT NULL,
    gender public.valid_gender NOT NULL,
    alamat text,
    email character varying NOT NULL,
    notelp character(13)
);
    DROP TABLE public.customer;
       public         heap    postgres    false    643            ?            1259    17756    customer_id_seq    SEQUENCE     x   CREATE SEQUENCE public.customer_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.customer_id_seq;
       public          postgres    false    216            7           0    0    customer_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.customer_id_seq OWNED BY public.customer.idcust;
          public          postgres    false    215            ?            1259    17654    event_id_seq    SEQUENCE     u   CREATE SEQUENCE public.event_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.event_id_seq;
       public          postgres    false            ?            1259    17661    event    TABLE     t  CREATE TABLE public.event (
    idevent character(4) DEFAULT ('E'::text || nextval('public.event_id_seq'::regclass)) NOT NULL,
    namaevent character varying(30) NOT NULL,
    tglevent date NOT NULL,
    jenisevent character varying,
    lokasievent text NOT NULL,
    deskripsi text,
    linkformdaftar character varying NOT NULL,
    status public.status_t NOT NULL
);
    DROP TABLE public.event;
       public         heap    postgres    false    206    668            ?            1259    17606    feedback_id_seq    SEQUENCE     x   CREATE SEQUENCE public.feedback_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.feedback_id_seq;
       public          postgres    false            ?            1259    17620    feedbackblog    TABLE     !  CREATE TABLE public.feedbackblog (
    idfeedback character(8) DEFAULT ('KMN'::text || nextval('public.feedback_id_seq'::regclass)) NOT NULL,
    idresponden character(8) NOT NULL,
    idkonten character(5) NOT NULL,
    feedback text,
    tglpublish date DEFAULT CURRENT_DATE NOT NULL
);
     DROP TABLE public.feedbackblog;
       public         heap    postgres    false    202            ?            1259    17670    forumdiskusi_id_seq    SEQUENCE     |   CREATE SEQUENCE public.forumdiskusi_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.forumdiskusi_id_seq;
       public          postgres    false            ?            1259    17672    forumdiskusi    TABLE     Z  CREATE TABLE public.forumdiskusi (
    idforum character(8) DEFAULT ('F'::text || nextval('public.forumdiskusi_id_seq'::regclass)) NOT NULL,
    judulforum character varying(30) NOT NULL,
    namapengirim character varying(30) NOT NULL,
    tglpublish date DEFAULT CURRENT_DATE NOT NULL,
    deskripsi text,
    kategori character varying(30)
);
     DROP TABLE public.forumdiskusi;
       public         heap    postgres    false    208            ?            1259    17682    komentarforum_id_seq    SEQUENCE     }   CREATE SEQUENCE public.komentarforum_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE public.komentarforum_id_seq;
       public          postgres    false            ?            1259    17684    komentarforum    TABLE     '  CREATE TABLE public.komentarforum (
    idkomentar character(10) DEFAULT ('KMN'::text || nextval('public.komentarforum_id_seq'::regclass)) NOT NULL,
    idresponden character(8) NOT NULL,
    idforum character(8) NOT NULL,
    feedback text,
    tglpublish date DEFAULT CURRENT_DATE NOT NULL
);
 !   DROP TABLE public.komentarforum;
       public         heap    postgres    false    210            ?            1259    17608    konten_id_seq    SEQUENCE     v   CREATE SEQUENCE public.konten_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE public.konten_id_seq;
       public          postgres    false            ?            1259    17635    konten    TABLE     ?   CREATE TABLE public.konten (
    idkonten character(5) DEFAULT ('B'::text || nextval('public.konten_id_seq'::regclass)) NOT NULL,
    judulkonten character varying(30) NOT NULL,
    deskripsi text,
    idfeedback character(8)
);
    DROP TABLE public.konten;
       public         heap    postgres    false    203            ?            1259    17701    pengajuanforum_id_seq    SEQUENCE     ~   CREATE SEQUENCE public.pengajuanforum_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ,   DROP SEQUENCE public.pengajuanforum_id_seq;
       public          postgres    false            ?            1259    17703    pengajuanforum    TABLE     ?  CREATE TABLE public.pengajuanforum (
    idpengajuan character(4) DEFAULT ('P'::text || nextval('public.pengajuanforum_id_seq'::regclass)) NOT NULL,
    judulforum character varying(30) NOT NULL,
    idresponden character(8) NOT NULL,
    namapengirim character varying(30) NOT NULL,
    tglpublish date DEFAULT CURRENT_DATE NOT NULL,
    deskripsi text,
    kategori character varying(30),
    status public.valid_status DEFAULT 'Belum disetujui'::public.valid_status NOT NULL
);
 "   DROP TABLE public.pengajuanforum;
       public         heap    postgres    false    212    685    685            ?            1259    17595    produk    TABLE     s  CREATE TABLE public.produk (
    idproduk character(6) NOT NULL,
    namaproduk character varying(30) NOT NULL,
    batch integer NOT NULL,
    kategori public.valid_kategori NOT NULL,
    harga double precision NOT NULL,
    quantity integer NOT NULL,
    berat double precision NOT NULL,
    deskripsi text NOT NULL,
    photo bytea NOT NULL,
    link text NOT NULL
);
    DROP TABLE public.produk;
       public         heap    postgres    false    649            ?            1259    17593    produk_id_seq    SEQUENCE     v   CREATE SEQUENCE public.produk_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE public.produk_id_seq;
       public          postgres    false    201            8           0    0    produk_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.produk_id_seq OWNED BY public.produk.idproduk;
          public          postgres    false    200            ?            1259    17776 	   responden    TABLE     I   CREATE TABLE public.responden (
    idresponden character(8) NOT NULL
);
    DROP TABLE public.responden;
       public         heap    postgres    false            }           2604    17770    admin idadm    DEFAULT     v   ALTER TABLE ONLY public.admin ALTER COLUMN idadm SET DEFAULT ('A'::text || nextval('public.admin_id_seq'::regclass));
 :   ALTER TABLE public.admin ALTER COLUMN idadm DROP DEFAULT;
       public          postgres    false    214    217    217            |           2604    17761    customer idcust    DEFAULT     }   ALTER TABLE ONLY public.customer ALTER COLUMN idcust SET DEFAULT ('C'::text || nextval('public.customer_id_seq'::regclass));
 >   ALTER TABLE public.customer ALTER COLUMN idcust DROP DEFAULT;
       public          postgres    false    215    216    216            p           2604    17598    produk idproduk    DEFAULT     {   ALTER TABLE ONLY public.produk ALTER COLUMN idproduk SET DEFAULT ('P'::text || nextval('public.produk_id_seq'::regclass));
 >   ALTER TABLE public.produk ALTER COLUMN idproduk DROP DEFAULT;
       public          postgres    false    201    200    201            -          0    17767    admin 
   TABLE DATA           Z   COPY public.admin (idadm, nama, username, password, jabatan, jobdesc, notelp) FROM stdin;
    public          postgres    false    217   ?X       ,          0    17758    customer 
   TABLE DATA           g   COPY public.customer (idcust, namacust, username, password, gender, alamat, email, notelp) FROM stdin;
    public          postgres    false    216   AY       #          0    17661    event 
   TABLE DATA           y   COPY public.event (idevent, namaevent, tglevent, jenisevent, lokasievent, deskripsi, linkformdaftar, status) FROM stdin;
    public          postgres    false    207   ?Y                  0    17620    feedbackblog 
   TABLE DATA           _   COPY public.feedbackblog (idfeedback, idresponden, idkonten, feedback, tglpublish) FROM stdin;
    public          postgres    false    204   ?Y       %          0    17672    forumdiskusi 
   TABLE DATA           j   COPY public.forumdiskusi (idforum, judulforum, namapengirim, tglpublish, deskripsi, kategori) FROM stdin;
    public          postgres    false    209   ?Y       '          0    17684    komentarforum 
   TABLE DATA           _   COPY public.komentarforum (idkomentar, idresponden, idforum, feedback, tglpublish) FROM stdin;
    public          postgres    false    211   ?Y       !          0    17635    konten 
   TABLE DATA           N   COPY public.konten (idkonten, judulkonten, deskripsi, idfeedback) FROM stdin;
    public          postgres    false    205   Z       )          0    17703    pengajuanforum 
   TABLE DATA           ?   COPY public.pengajuanforum (idpengajuan, judulforum, idresponden, namapengirim, tglpublish, deskripsi, kategori, status) FROM stdin;
    public          postgres    false    213   2Z                 0    17595    produk 
   TABLE DATA           w   COPY public.produk (idproduk, namaproduk, batch, kategori, harga, quantity, berat, deskripsi, photo, link) FROM stdin;
    public          postgres    false    201   OZ       .          0    17776 	   responden 
   TABLE DATA           0   COPY public.responden (idresponden) FROM stdin;
    public          postgres    false    218   lZ       9           0    0    admin_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.admin_id_seq', 1, true);
          public          postgres    false    214            :           0    0    customer_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.customer_id_seq', 1, true);
          public          postgres    false    215            ;           0    0    event_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.event_id_seq', 1, false);
          public          postgres    false    206            <           0    0    feedback_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.feedback_id_seq', 1, false);
          public          postgres    false    202            =           0    0    forumdiskusi_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.forumdiskusi_id_seq', 1, false);
          public          postgres    false    208            >           0    0    komentarforum_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.komentarforum_id_seq', 1, false);
          public          postgres    false    210            ?           0    0    konten_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.konten_id_seq', 1, false);
          public          postgres    false    203            @           0    0    pengajuanforum_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public.pengajuanforum_id_seq', 1, false);
          public          postgres    false    212            A           0    0    produk_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.produk_id_seq', 1, false);
          public          postgres    false    200            ?           2606    17775    admin admin_pkey 
   CONSTRAINT     Q   ALTER TABLE ONLY public.admin
    ADD CONSTRAINT admin_pkey PRIMARY KEY (idadm);
 :   ALTER TABLE ONLY public.admin DROP CONSTRAINT admin_pkey;
       public            postgres    false    217            ?           2606    17766    customer customer_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.customer
    ADD CONSTRAINT customer_pkey PRIMARY KEY (idcust);
 @   ALTER TABLE ONLY public.customer DROP CONSTRAINT customer_pkey;
       public            postgres    false    216            ?           2606    17669    event event_pkey 
   CONSTRAINT     S   ALTER TABLE ONLY public.event
    ADD CONSTRAINT event_pkey PRIMARY KEY (idevent);
 :   ALTER TABLE ONLY public.event DROP CONSTRAINT event_pkey;
       public            postgres    false    207            ?           2606    17629    feedbackblog feedbackblog_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.feedbackblog
    ADD CONSTRAINT feedbackblog_pkey PRIMARY KEY (idfeedback);
 H   ALTER TABLE ONLY public.feedbackblog DROP CONSTRAINT feedbackblog_pkey;
       public            postgres    false    204            ?           2606    17681    forumdiskusi forumdiskusi_pkey 
   CONSTRAINT     a   ALTER TABLE ONLY public.forumdiskusi
    ADD CONSTRAINT forumdiskusi_pkey PRIMARY KEY (idforum);
 H   ALTER TABLE ONLY public.forumdiskusi DROP CONSTRAINT forumdiskusi_pkey;
       public            postgres    false    209            ?           2606    17693     komentarforum komentarforum_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.komentarforum
    ADD CONSTRAINT komentarforum_pkey PRIMARY KEY (idkomentar);
 J   ALTER TABLE ONLY public.komentarforum DROP CONSTRAINT komentarforum_pkey;
       public            postgres    false    211            ?           2606    17643    konten konten_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.konten
    ADD CONSTRAINT konten_pkey PRIMARY KEY (idkonten);
 <   ALTER TABLE ONLY public.konten DROP CONSTRAINT konten_pkey;
       public            postgres    false    205            ?           2606    17713 "   pengajuanforum pengajuanforum_pkey 
   CONSTRAINT     i   ALTER TABLE ONLY public.pengajuanforum
    ADD CONSTRAINT pengajuanforum_pkey PRIMARY KEY (idpengajuan);
 L   ALTER TABLE ONLY public.pengajuanforum DROP CONSTRAINT pengajuanforum_pkey;
       public            postgres    false    213                       2606    17603    produk produk_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.produk
    ADD CONSTRAINT produk_pkey PRIMARY KEY (idproduk);
 <   ALTER TABLE ONLY public.produk DROP CONSTRAINT produk_pkey;
       public            postgres    false    201            ?           2606    17780    responden responden_pkey 
   CONSTRAINT     _   ALTER TABLE ONLY public.responden
    ADD CONSTRAINT responden_pkey PRIMARY KEY (idresponden);
 B   ALTER TABLE ONLY public.responden DROP CONSTRAINT responden_pkey;
       public            postgres    false    218            ?           2620    17781     customer trigger_isi_idresponden    TRIGGER     ?   CREATE TRIGGER trigger_isi_idresponden AFTER INSERT OR DELETE ON public.customer FOR EACH ROW EXECUTE FUNCTION public.isiidresponden();
 9   DROP TRIGGER trigger_isi_idresponden ON public.customer;
       public          postgres    false    216    219            ?           2620    17782 "   admin trigger_isi_idrespondenadmin    TRIGGER     ?   CREATE TRIGGER trigger_isi_idrespondenadmin AFTER INSERT OR DELETE ON public.admin FOR EACH ROW EXECUTE FUNCTION public.isiidrespondenadmin();
 ;   DROP TRIGGER trigger_isi_idrespondenadmin ON public.admin;
       public          postgres    false    217    220            ?           2606    17644    konten fk_feedback    FK CONSTRAINT     ?   ALTER TABLE ONLY public.konten
    ADD CONSTRAINT fk_feedback FOREIGN KEY (idfeedback) REFERENCES public.feedbackblog(idfeedback) ON DELETE SET NULL;
 <   ALTER TABLE ONLY public.konten DROP CONSTRAINT fk_feedback;
       public          postgres    false    204    205    2945            ?           2606    17744    komentarforum fk_idforum    FK CONSTRAINT     ?   ALTER TABLE ONLY public.komentarforum
    ADD CONSTRAINT fk_idforum FOREIGN KEY (idforum) REFERENCES public.forumdiskusi(idforum);
 B   ALTER TABLE ONLY public.komentarforum DROP CONSTRAINT fk_idforum;
       public          postgres    false    2951    209    211            ?           2606    17788    komentarforum fk_idrespondenadm    FK CONSTRAINT     ?   ALTER TABLE ONLY public.komentarforum
    ADD CONSTRAINT fk_idrespondenadm FOREIGN KEY (idresponden) REFERENCES public.admin(idadm);
 I   ALTER TABLE ONLY public.komentarforum DROP CONSTRAINT fk_idrespondenadm;
       public          postgres    false    2959    211    217            ?           2606    17783     komentarforum fk_idrespondencust    FK CONSTRAINT     ?   ALTER TABLE ONLY public.komentarforum
    ADD CONSTRAINT fk_idrespondencust FOREIGN KEY (idresponden) REFERENCES public.customer(idcust);
 J   ALTER TABLE ONLY public.komentarforum DROP CONSTRAINT fk_idrespondencust;
       public          postgres    false    211    2957    216            ?           2606    17649    feedbackblog fk_konten    FK CONSTRAINT     }   ALTER TABLE ONLY public.feedbackblog
    ADD CONSTRAINT fk_konten FOREIGN KEY (idkonten) REFERENCES public.konten(idkonten);
 @   ALTER TABLE ONLY public.feedbackblog DROP CONSTRAINT fk_konten;
       public          postgres    false    2947    205    204            ?           2606    17793    feedbackblog fk_responden    FK CONSTRAINT     ?   ALTER TABLE ONLY public.feedbackblog
    ADD CONSTRAINT fk_responden FOREIGN KEY (idresponden) REFERENCES public.responden(idresponden);
 C   ALTER TABLE ONLY public.feedbackblog DROP CONSTRAINT fk_responden;
       public          postgres    false    204    2961    218            -   2   x?s4T μĔ̢D(???YQQ???????f@?
?=... ??\      ,   P   x?s6T μĔ̢D(???YQQ??Z??[P??Ǚ??????XdC?8??&f??%??rXZX???T(p??qqq ?L?      #      x?????? ? ?             x?????? ? ?      %      x?????? ? ?      '      x?????? ? ?      !      x?????? ? ?      )      x?????? ? ?            x?????? ? ?      .      x?s6T .G#F??? (?#     