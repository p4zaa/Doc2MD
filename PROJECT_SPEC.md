# Project Specification: Web Document to Markdown Converter

## 1. Project Overview
The **Web Document to Markdown Converter** is a tool that takes the main URL of a document-based website and automatically:
1. Crawls through all pages under the document domain.
2. Converts each page into clean **Markdown (.md)** format.
3. Saves the output into a **nested folder structure** that mirrors the original document hierarchy.
4. Generates a **link tree** for easy navigation of all converted Markdown files.

## 2. Objectives
- Provide a simple way to archive online documentation in Markdown format.
- Support flexible crawling depth control.
- Maintain internal links for offline viewing and easy navigation.
- Preserve document structure with a clear folder hierarchy.

## 3. Key Features
- **Main URL Input**: Users specify the root URL of the documentation site.
- **Link Depth Control**: 
  - `depth = 0` → Crawl all links under the same domain.
  - `depth = N` → Limit crawling to N levels deep.
- **Markdown Conversion**:
  - Convert HTML content to clean Markdown.
  - Strip unnecessary styles/scripts.
  - Preserve headings, paragraphs, lists, tables, images, and internal links.
- **Folder Structure**:
  - Create nested folders representing the site's structure.
  - Store each page as `index.md` or `page_name.md`.
- **Link Tree Generation**:
  - Create a root `README.md` with a tree-like structure linking all pages.

## 4. Inputs & Outputs
### Input
- **Main URL** (string): Starting point of the documentation.
- **Depth Level** (int): Depth limit for crawling links (0 for unlimited).

### Output
- **Markdown Files**: For each page in the site.
- **Folder Structure**: Nested folders replicating site hierarchy.
- **Navigation Tree**: `README.md` with a link tree of all pages.

## 5. Example
**Input**:
```
URL: https://google.github.io/adk-docs/
Depth: 2
```

**Output Structure**:
```
docs/
 ├── README.md
 ├── index.md
 ├── getting-started/
 │    ├── index.md
 │    └── installation.md
 └── guides/
      ├── index.md
      ├── advanced/
      │    └── tips.md
      └── faq.md
```

## 6. Technical Details
- **Language**: Python or Go (to be decided).
- **Libraries**:
  - Web crawling: `requests`, `beautifulsoup4`, or `playwright` (if needed).
  - Markdown conversion: `html2text` or custom parser.
- **Link Tree Generation**: Recursively scan folders and generate Markdown links.

## 7. Constraints & Assumptions
- Only internal links under the same domain will be crawled.
- No authentication or paywalled content.
- Site must be static or partially dynamic but crawlable.

## 8. Future Enhancements
- Option to export as **PDF** or **single Markdown file**.
- Integration with **GitHub Pages** for hosting.
- Support for **incremental updates** instead of full re-crawling.

## 9. Milestones
1. **MVP**: Crawl and convert pages to Markdown with depth control.
2. **Phase 2**: Nested folder output + link tree generation.
3. **Phase 3**: Configurable options, UI, and advanced features.