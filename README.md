# fortify_translate
# 使用说明
1. 生成报告，选择Tools->Reports->Generate BIRT Report，选择Develop Workbook模板，生成html文件
2. 执行以下命令
```python
python html2xls.py <html_filename> <xlsx_filename>
```
* html_filename：生成的HTML格式的报告
* xlsx_filename：自定义的XLSX文件名称
