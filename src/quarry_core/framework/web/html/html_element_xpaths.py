from typing import Final, List


class HTMLElementXPaths:
    """
    A class containing constants for XPath expressions used to select various HTML elements.
    These selectors are typically used for identifying elements to be excluded or processed in HTML parsing.
    """

    HEADER: Final[List[str]] = [
        "//header",
        '//*[contains(@class, "header")]',
        '//*[contains(@id, "header")]',
    ]

    FOOTER: Final[List[str]] = [
        "//footer",
        '//*[contains(@class, "footer")]',
        '//*[contains(@id, "footer")]',
    ]

    NAV: Final[List[str]] = [
        "//nav",
        "//aside",
        '//*[contains(@class, "menu")]',
        '//*[contains(@class, "navigation")]',
        '//*[contains(@class, "sidebar")]',
        '//*[contains(@id, "sidebar")]',
        '//*[contains(@class, "nav")]',
        '//*[contains(@id, "nav")]',
    ]

    COMMENTS: Final[List[str]] = [
        '//*[contains(@class, "comment")]',
        '//*[contains(@id, "comment")]',
        '//*[contains(@class, "disqus")]',
    ]

    SOCIAL: Final[List[str]] = [
        '//*[contains(@class, "social")]',
        '//*[contains(@class, "share")]',
        '//*[contains(@class, "twitter")]',
        '//*[contains(@class, "facebook")]',
        '//*[contains(@class, "linkedin")]',
    ]

    ADS: Final[List[str]] = [
        '//*[contains(@class, "ad")]',
        '//*[contains(@class, "ads")]',
        '//*[contains(@class, "advertisement")]',
        '//*[contains(@id, "ad")]',
        '//*[contains(@id, "ads")]',
        '//ins[contains(@class, "adsbygoogle")]',
    ]

    MISC: Final[List[str]] = [
        "//script",
        "//form",
        '//*[contains(@class, "related")]',
        '//*[contains(@class, "widget")]',
        '//*[contains(@class, "cookie")]',
        '//*[contains(@class, "popup")]',
        '//*[contains(@class, "banner")]',
    ]

    ARTICLE: List[str] = [
        ".//main",
        './/*[@role="main"]',
        './/*[contains(@class, "main")]',
        './/*[contains(@class, "content")]',
        ".//article",
        './/div[contains(@class, "post")]',
        './/*[contains(@class, "entry")]',
        './/*[contains(@itemprop, "articleBody")]',
    ]

    AUTHOR: List[str] = [
        '//meta[@name="author"]/@content',
        '//meta[@name="article:author"]/@content',
        '//meta[@property="article:author"]/@content',
        '//meta[@property="og:author"]/@content',
        '//span[contains(@class, "author")]/text()',
        '//a[contains(@class, "author")]/text()',
        '//p[contains(@class, "author")]/text()',
        '//*[contains(@class, "author")]/text()',
        '//meta[@name="sailthru.author"]/@content',
        '//a[contains(@rel, "author")]/text()',
        '//span[contains(@itemprop, "author")]/text()',
        '//div[contains(@class, "author-name")]/text()',
        '//span[contains(@class, "fn")]/text()',
        '//*[@itemprop="author"]/*[@itemprop="name"]/text()',
    ]

    PUBLISHED_TIME: List[str] = [
        '//meta[@property="article:published_time"]/@content',
        '//meta[@property="og:published_time"]/@content',
        "//time[@pubdate]/@datetime",
        '//time[@itemprop="datePublished"]/@datetime',
        '//meta[@name="date"]/@content',
        '//meta[@name="DC.date.issued"]/@content',
        '//span[@class="published"]/@title',
        '//meta[@property="article:published"]/@content',
        '//meta[@itemprop="datePublished"]/@content',
        '//abbr[@class="published"]/@title',
        '//*[contains(@class, "published")]/@datetime',
        '//*[contains(@class, "date")]/@datetime',
        '//*[contains(@class, "date")]/text()',
    ]

    TITLE: List[str] = [
        '//meta[@property="og:title"]/@content',
        '//meta[@name="title"]/@content',
        '//h1[contains(@class, "title")]/text()',
        '//h1[contains(@class, "headline")]/text()',
        '//h1/text()',
        "//title/text()",
        '//meta[@name="twitter:title"]/@content',
    ]

    DESCRIPTION: List[str] = ['//meta[@name="description"]/@content']

    KEYWORDS: List[str] = [
        '//meta[@name="keywords"]/@content',
        '//meta[@property="article:tag"]/@content',
    ]
