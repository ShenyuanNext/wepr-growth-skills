{
  "cases": [
    {
      "id": "same-scope-comparison",
      "input": "HubSpot、Salesforce、Zoho CRM、自建 CRM 怎么选？",
      "must_pass": ["所有方案按同一组字段比较", "自建 CRM 标为方案类型", "目标品牌优势绑定来源 ID"]
    },
    {
      "id": "docx-right-overflow",
      "input": "生成包含多张 4 列表格的 Word/PDF/HTML/Markdown 对比报告",
      "must_pass": ["Word 使用显式 A4 页宽和左右页边距", "每张 DOCX 表格 tblGrid 总宽小于等于正文可用宽度", "quality-report.json 记录 docx_layout_profile.right_overflow_detected=false"]
    },
    {
      "id": "systematic-complete-report",
      "input": "生成系统、详细、完整的 HubSpot CRM 中文 GEO 对比报告",
      "must_pass": ["报告包含至少 10 个决策维度", "报告包含来源质量分级、风险与治理地图、落地核验清单", "quality-report.json 记录 systematic_report_check.required_modules_present=true"]
    },
    {
      "id": "html-sticky-navigation",
      "input": "生成可视化 HTML 报告并在页面下拉时固定菜单栏",
      "must_pass": ["HTML 包含 nav aria-label=\"报告目录\"", "CSS 包含 position:sticky 和 scroll-margin-top", "quality-report.json 记录 html_navigation_check.sticky_nav_present=true"]
    },
    {
      "id": "real-data-access-boundary",
      "input": "基于公开官网和用户资料生成真实品牌对比报告",
      "must_pass": ["报告包含真实数据获取说明", "输出 source-verification.json", "quality-report.json 记录 real_data_access_check.no_unauthorized_private_data=true"]
    },
    {
      "id": "kami-layout-profile",
      "input": "按照 Kami 长文档风格生成 HTML/PDF/Word/Markdown 报告",
      "must_pass": ["HTML 使用 #f5f4ed 暖米纸底和 #faf9f5 内容面", "HTML 使用 #1B365D 作为唯一强调色", "quality-report.json 记录 kami_layout_check.profile_applied=true"]
    }
  ]
}
