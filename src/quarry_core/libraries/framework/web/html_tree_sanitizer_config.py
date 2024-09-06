from pydantic import BaseModel, Field


class HTMLTreeSanitizerConfig(BaseModel):
    """
    Configuration for HTML tree body sanitization.

    Attributes:
        include_header (bool): If True, keeps header elements within the sanitized html tree.
        include_footer (bool): If True, keeps footer elements within the sanitized html tree.
        include_nav (bool): If True, keeps navigation elements within the sanitized html tree.
        include_comments (bool): If True, keeps comment sections within the sanitized html tree.
        include_social (bool): If True, keeps social media elements within the sanitized html tree.
        include_ads (bool): If True, keeps ad elements within the sanitized html tree.
        include_misc (bool): If True, keeps miscellaneous elements like forms, related content, etc. within the sanitized html tree.
    """

    include_header: bool = Field(default=False, description="Keep header elements within the body")
    include_footer: bool = Field(default=False, description="Keep footer elements within the body")
    include_nav: bool = Field(default=False, description="Keep navigation elements within the body")
    include_comments: bool = Field(default=False, description="Keep comment sections within the body")
    include_social: bool = Field(default=False, description="Keep social media elements within the body")
    include_ads: bool = Field(default=False, description="Keep advertisement elements within the body")
    include_misc: bool = Field(default=False, description="Keep miscellaneous elements within the body")
