USE [product_matching]
GO

/****** Object:  Table [dbo].[product_matching_results]    Script Date: 7/16/2021 2:34:32 PM ******/
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
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO