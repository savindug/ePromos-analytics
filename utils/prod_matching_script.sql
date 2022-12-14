USE [master]
GO
/****** Object:  Database [product_matching]    Script Date: 8/7/2021 4:26:45 PM ******/
CREATE DATABASE [product_matching]
 CONTAINMENT = NONE
 ON  PRIMARY 
( NAME = N'produt_matching', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL15.SQLEXPRESS\MSSQL\DATA\produt_matching.mdf' , SIZE = 73728KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536KB )
 LOG ON 
( NAME = N'produt_matching_log', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL15.SQLEXPRESS\MSSQL\DATA\produt_matching_log.ldf' , SIZE = 8192KB , MAXSIZE = 2048GB , FILEGROWTH = 65536KB )
 WITH CATALOG_COLLATION = DATABASE_DEFAULT
GO
ALTER DATABASE [product_matching] SET COMPATIBILITY_LEVEL = 150
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [product_matching].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [product_matching] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [product_matching] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [product_matching] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [product_matching] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [product_matching] SET ARITHABORT OFF 
GO
ALTER DATABASE [product_matching] SET AUTO_CLOSE ON 
GO
ALTER DATABASE [product_matching] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [product_matching] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [product_matching] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [product_matching] SET CURSOR_DEFAULT  GLOBAL 
GO
ALTER DATABASE [product_matching] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [product_matching] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [product_matching] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [product_matching] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [product_matching] SET  ENABLE_BROKER 
GO
ALTER DATABASE [product_matching] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [product_matching] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [product_matching] SET TRUSTWORTHY OFF 
GO
ALTER DATABASE [product_matching] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO
ALTER DATABASE [product_matching] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [product_matching] SET READ_COMMITTED_SNAPSHOT OFF 
GO
ALTER DATABASE [product_matching] SET HONOR_BROKER_PRIORITY OFF 
GO
ALTER DATABASE [product_matching] SET RECOVERY SIMPLE 
GO
ALTER DATABASE [product_matching] SET  MULTI_USER 
GO
ALTER DATABASE [product_matching] SET PAGE_VERIFY CHECKSUM  
GO
ALTER DATABASE [product_matching] SET DB_CHAINING OFF 
GO
ALTER DATABASE [product_matching] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
GO
ALTER DATABASE [product_matching] SET TARGET_RECOVERY_TIME = 60 SECONDS 
GO
ALTER DATABASE [product_matching] SET DELAYED_DURABILITY = DISABLED 
GO
ALTER DATABASE [product_matching] SET QUERY_STORE = OFF
GO
USE [product_matching]
GO
/****** Object:  Schema [m2ss]    Script Date: 8/7/2021 4:26:45 PM ******/
CREATE SCHEMA [m2ss]
GO
/****** Object:  Schema [product_matching]    Script Date: 8/7/2021 4:26:45 PM ******/
CREATE SCHEMA [product_matching]
GO
/****** Object:  Table [dbo].[product_matching_results]    Script Date: 8/7/2021 4:26:45 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[product_matching_results](
	[id] [int] IDENTITY(3856,1) NOT NULL,
	[epromos_productId] [varchar](max) NULL,
	[epromos_productName] [varchar](max) NULL,
	[vendorsKU] [varchar](max) NULL,
	[venderName] [varchar](max) NULL,
	[4imprint_product_url] [varchar](max) NULL,
	[product_name_matching] [varchar](max) NULL,
	[product_material_matching] [varchar](max) NULL,
	[product_desc_matching] [varchar](max) NULL,
	[product_keyword_matching] [varchar](max) NULL,
	[created] [datetime] NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [product_matching].[4imprint_categories]    Script Date: 8/7/2021 4:26:45 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [product_matching].[4imprint_categories](
	[id] [int] IDENTITY(77,1) NOT NULL,
	[catID] [varchar](250) NOT NULL,
	[name] [varchar](250) NOT NULL,
	[category_page] [varchar](max) NOT NULL,
	[table_slug] [varchar](255) NOT NULL,
	[type] [varchar](max) NULL,
	[created] [datetime] NOT NULL,
 CONSTRAINT [PK_4imprint_categories_id] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [product_matching].[4imprint_products]    Script Date: 8/7/2021 4:26:45 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [product_matching].[4imprint_products](
	[id] [int] IDENTITY(3856,1) NOT NULL,
	[code] [varchar](250) NOT NULL,
	[name] [varchar](250) NOT NULL,
	[price] [varchar](250) NOT NULL,
	[product_page] [varchar](max) NOT NULL,
	[img] [varchar](max) NOT NULL,
	[desc] [varchar](max) NOT NULL,
	[category] [varchar](max) NOT NULL,
	[created] [datetime] NOT NULL,
	[size] [nchar](10) NULL,
 CONSTRAINT [PK_4imprint_products_id] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [product_matching].[4imprint_products_prices]    Script Date: 8/7/2021 4:26:45 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [product_matching].[4imprint_products_prices](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[sku] [varchar](250) NOT NULL,
	[name] [varchar](250) NOT NULL,
	[url] [varchar](max) NOT NULL,
	[entryType] [varchar](max) NOT NULL,
	[order] [varchar](max) NOT NULL,
	[value] [varchar](max) NOT NULL,
	[setupCharge] [varchar](max) NOT NULL,
	[setupDesc] [varchar](max) NOT NULL,
	[priceBreakCount] [varchar](max) NOT NULL,
	[created] [datetime] NOT NULL,
 CONSTRAINT [PK_4imprint_products_prices_id] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [product_matching].[4imprint_sub_categories]    Script Date: 8/7/2021 4:26:45 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [product_matching].[4imprint_sub_categories](
	[id] [int] IDENTITY(504,1) NOT NULL,
	[catID] [varchar](250) NOT NULL,
	[parent_category] [varchar](250) NOT NULL,
	[name] [varchar](250) NOT NULL,
	[category_page] [varchar](max) NOT NULL,
	[created] [datetime] NOT NULL,
 CONSTRAINT [PK_4imprint_sub_categories_id] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [product_matching].[epromos_materials_table]    Script Date: 8/7/2021 4:26:45 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [product_matching].[epromos_materials_table](
	[id] [int] IDENTITY(201,1) NOT NULL,
	[materialId] [int] NULL,
	[materialName] [varchar](max) NULL,
 CONSTRAINT [PK_epromos_materials_table_id] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [product_matching].[epromos_products]    Script Date: 8/7/2021 4:26:45 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [product_matching].[epromos_products](
	[name] [varchar](max) NULL,
	[productId] [int] NULL,
	[seoUrl] [varchar](max) NULL,
	[vendorsKU] [varchar](max) NULL,
	[categoryId] [int] NULL,
	[category] [varchar](max) NULL,
	[metaDescription] [varchar](max) NULL,
	[longDescription] [varchar](max) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [product_matching].[epromos_products_and_categories]    Script Date: 8/7/2021 4:26:45 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [product_matching].[epromos_products_and_categories](
	[name] [varchar](max) NULL,
	[productId] [int] NULL,
	[seoUrl] [varchar](max) NULL,
	[vendorsKU] [varchar](max) NULL,
	[categoryId] [int] NULL,
	[category] [varchar](max) NULL,
	[metaDescription] [varchar](max) NULL,
	[longDescription] [varchar](max) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
ALTER TABLE [dbo].[product_matching_results] ADD  DEFAULT (getdate()) FOR [created]
GO
ALTER TABLE [product_matching].[4imprint_categories] ADD  DEFAULT (NULL) FOR [type]
GO
ALTER TABLE [product_matching].[4imprint_categories] ADD  DEFAULT (getdate()) FOR [created]
GO
ALTER TABLE [product_matching].[4imprint_products] ADD  DEFAULT (getdate()) FOR [created]
GO
ALTER TABLE [product_matching].[4imprint_products_prices] ADD  DEFAULT (getdate()) FOR [created]
GO
ALTER TABLE [product_matching].[4imprint_sub_categories] ADD  DEFAULT (getdate()) FOR [created]
GO
ALTER TABLE [product_matching].[epromos_materials_table] ADD  DEFAULT (NULL) FOR [materialId]
GO
ALTER TABLE [product_matching].[epromos_materials_table] ADD  DEFAULT (NULL) FOR [materialName]
GO
ALTER TABLE [product_matching].[epromos_products] ADD  DEFAULT (NULL) FOR [name]
GO
ALTER TABLE [product_matching].[epromos_products] ADD  DEFAULT (NULL) FOR [productId]
GO
ALTER TABLE [product_matching].[epromos_products] ADD  DEFAULT (NULL) FOR [seoUrl]
GO
ALTER TABLE [product_matching].[epromos_products] ADD  DEFAULT (NULL) FOR [vendorsKU]
GO
ALTER TABLE [product_matching].[epromos_products] ADD  DEFAULT (NULL) FOR [categoryId]
GO
ALTER TABLE [product_matching].[epromos_products] ADD  DEFAULT (NULL) FOR [category]
GO
ALTER TABLE [product_matching].[epromos_products] ADD  DEFAULT (NULL) FOR [metaDescription]
GO
ALTER TABLE [product_matching].[epromos_products] ADD  DEFAULT (NULL) FOR [longDescription]
GO
ALTER TABLE [product_matching].[epromos_products_and_categories] ADD  DEFAULT (NULL) FOR [name]
GO
ALTER TABLE [product_matching].[epromos_products_and_categories] ADD  DEFAULT (NULL) FOR [productId]
GO
ALTER TABLE [product_matching].[epromos_products_and_categories] ADD  DEFAULT (NULL) FOR [seoUrl]
GO
ALTER TABLE [product_matching].[epromos_products_and_categories] ADD  DEFAULT (NULL) FOR [vendorsKU]
GO
ALTER TABLE [product_matching].[epromos_products_and_categories] ADD  DEFAULT (NULL) FOR [categoryId]
GO
ALTER TABLE [product_matching].[epromos_products_and_categories] ADD  DEFAULT (NULL) FOR [category]
GO
ALTER TABLE [product_matching].[epromos_products_and_categories] ADD  DEFAULT (NULL) FOR [metaDescription]
GO
ALTER TABLE [product_matching].[epromos_products_and_categories] ADD  DEFAULT (NULL) FOR [longDescription]
GO
EXEC sys.sp_addextendedproperty @name=N'MS_SSMA_SOURCE', @value=N'product_matching.4imprint_categories' , @level0type=N'SCHEMA',@level0name=N'product_matching', @level1type=N'TABLE',@level1name=N'4imprint_categories'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_SSMA_SOURCE', @value=N'product_matching.4imprint_products' , @level0type=N'SCHEMA',@level0name=N'product_matching', @level1type=N'TABLE',@level1name=N'4imprint_products'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_SSMA_SOURCE', @value=N'product_matching.4imprint_sub_categories' , @level0type=N'SCHEMA',@level0name=N'product_matching', @level1type=N'TABLE',@level1name=N'4imprint_sub_categories'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_SSMA_SOURCE', @value=N'product_matching.epromos_materials_table' , @level0type=N'SCHEMA',@level0name=N'product_matching', @level1type=N'TABLE',@level1name=N'epromos_materials_table'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_SSMA_SOURCE', @value=N'product_matching.epromos_products' , @level0type=N'SCHEMA',@level0name=N'product_matching', @level1type=N'TABLE',@level1name=N'epromos_products'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_SSMA_SOURCE', @value=N'product_matching.epromos_products_and_categories' , @level0type=N'SCHEMA',@level0name=N'product_matching', @level1type=N'TABLE',@level1name=N'epromos_products_and_categories'
GO
USE [master]
GO
ALTER DATABASE [product_matching] SET  READ_WRITE 
GO
