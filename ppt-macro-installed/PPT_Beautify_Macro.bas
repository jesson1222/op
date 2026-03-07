' ============================================================
' PowerPoint VBA 宏 - 自动美化个人简介 PPT
' 功能：一键应用专业配色、字体、布局
' 作者：OpenClaw AI Assistant
' 日期：2026 年 3 月 4 日
' ============================================================

Option Explicit

' 配色方案定义
Const COLOR_PRIMARY As String = "#1e3a8a"      ' 深蓝色 - 主色
Const COLOR_SECONDARY As String = "#3b82f6"    ' 浅蓝色 - 辅助色
Const COLOR_ACCENT As String = "#f59e0b"       ' 金色 - 强调色
Const COLOR_BG As String = "#ffffff"           ' 白色 - 背景
Const COLOR_TEXT As String = "#1f2937"         ' 深灰 - 文字
Const COLOR_BG_LIGHT As String = "#f9fafb"     ' 浅灰 - 浅背景

' ============================================================
' 主函数 - 一键美化
' ============================================================
Sub BeautifyPresentation()
    On Error GoTo ErrorHandler
    
    Dim ppt As Presentation
    Dim slide As slide
    Dim shp As Shape
    Dim i As Integer
    
    Set ppt = ActivePresentation
    
    ' 显示进度提示
    MsgBox "开始美化演示文稿..." & vbCrLf & vbCrLf & _
           "将应用以下优化：" & vbCrLf & _
           "• 统一配色方案（深蓝色主题）" & vbCrLf & _
           "• 优化字体层次" & vbCrLf & _
           "• 调整布局和对齐" & vbCrLf & _
           "• 增加专业视觉效果", _
           vbInformation, "PPT 美化工具"
    
    ' 1. 设置幻灯片母版
    Call SetupMasterSlide(ppt)
    
    ' 2. 优化每张幻灯片
    For Each slide In ppt.Slides
        Call OptimizeSlide(slide)
    Next slide
    
    ' 3. 添加页脚和页码
    Call AddFooter(ppt)
    
    ' 4. 应用平滑过渡效果
    Call ApplyTransitions(ppt)
    
    MsgBox "✓ 美化完成！" & vbCrLf & vbCrLf & _
           "已应用专业设计优化。" & vbCrLf & _
           "建议：检查每页内容，根据需要微调。", _
           vbInformation, "美化完成"
    
    Exit Sub

ErrorHandler:
    MsgBox "✗ 发生错误：" & Err.Description & vbCrLf & _
           "请确保宏权限已启用。", _
           vbCritical, "错误"
End Sub

' ============================================================
' 设置幻灯片母版
' ============================================================
Sub SetupMasterSlide(ppt As Presentation)
    Dim master As CustomLayout
    Dim shp As Shape
    
    ' 设置背景色
    ppt.SlideMaster.Background.Fill.ForeColor.RGB = HexToColor(COLOR_BG)
    
    ' 添加顶部装饰条
    Set shp = ppt.SlideMaster.Shapes.AddShape( _
        Type:=msoShapeRectangle, _
        Left:=0, Top:=0, _
        Width:=ppt.PageSetup.SlideWidth, _
        Height:=8)
    
    With shp
        .Fill.ForeColor.RGB = HexToColor(COLOR_PRIMARY)
        .Line.Visible = msoFalse
        .ZOrder msoSendToBack
    End With
    
    ' 设置默认字体
    With ppt.SlideMaster.TextStyles(ppDefaultTextStyle)
        .TextFrame.TextRange.Font.Name = "微软雅黑"
        .TextFrame.TextRange.Font.Size = 18
        .TextFrame.TextRange.Font.Color.RGB = HexToColor(COLOR_TEXT)
    End With
    
    ' 设置标题字体
    With ppt.SlideMaster.TextStyles(ppTitleTextStyle)
        .TextFrame.TextRange.Font.Name = "微软雅黑"
        .TextFrame.TextRange.Font.Size = 40
        .TextFrame.TextRange.Font.Bold = msoTrue
        .TextFrame.TextRange.Font.Color.RGB = HexToColor(COLOR_PRIMARY)
    End With
End Sub

' ============================================================
' 优化单张幻灯片
' ============================================================
Sub OptimizeSlide(slide As slide)
    Dim shp As Shape
    Dim txtRng As TextRange
    Dim i As Integer
    
    ' 优化每个形状
    For Each shp In slide.Shapes
        Call OptimizeShape(shp)
    Next shp
    
    ' 确保内容对齐
    Call AlignContent(slide)
End Sub

' ============================================================
' 优化单个形状
' ============================================================
Sub OptimizeShape(shp As Shape)
    On Error Resume Next
    
    Dim txtRng As TextRange
    
    ' 如果是文本框
    If shp.HasTextFrame Then
        If shp.TextFrame.HasText Then
            Set txtRng = shp.TextFrame.TextRange
            
            ' 根据文本内容判断类型并设置样式
            If InStr(1, txtRng.Text, "简介", vbTextCompare) > 0 Or _
               InStr(1, txtRng.Text, "简历", vbTextCompare) > 0 Or _
               InStr(1, txtRng.Text, "个人", vbTextCompare) > 0 Then
                ' 标题样式
                Call ApplyTitleStyle(txtRng)
            ElseIf InStr(1, txtRng.Text, "经历", vbTextCompare) > 0 Or _
                   InStr(1, txtRng.Text, "教育", vbTextCompare) > 0 Or _
                   InStr(1, txtRng.Text, "技能", vbTextCompare) > 0 Then
                ' 副标题样式
                Call ApplySubtitleStyle(txtRng)
            Else
                ' 正文样式
                Call ApplyBodyStyle(txtRng)
            End If
            
            ' 设置段落格式
            With txtRng.ParagraphFormat
                .LineRuleWithin = msoTrue
                .SpaceWithin = 1.5
                .SpaceBefore = 6
                .SpaceAfter = 6
            End With
        End If
    End If
    
    ' 优化形状样式
    If shp.Type = msoShape Then
        Call ApplyShapeStyle(shp)
    End If
End Sub

' ============================================================
' 应用标题样式
' ============================================================
Sub ApplyTitleStyle(txtRng As TextRange)
    With txtRng.Font
        .Name = "微软雅黑"
        .Size = 36
        .Bold = msoTrue
        .Color.RGB = HexToColor(COLOR_PRIMARY)
    End With
End Sub

' ============================================================
' 应用副标题样式
' ============================================================
Sub ApplySubtitleStyle(txtRng As TextRange)
    With txtRng.Font
        .Name = "微软雅黑"
        .Size = 24
        .Bold = msoTrue
        .Color.RGB = HexToColor(COLOR_SECONDARY)
    End With
End Sub

' ============================================================
' 应用正文样式
' ============================================================
Sub ApplyBodyStyle(txtRng As TextRange)
    With txtRng.Font
        .Name = "微软雅黑"
        .Size = 16
        .Bold = msoFalse
        .Color.RGB = HexToColor(COLOR_TEXT)
    End With
End Sub

' ============================================================
' 应用形状样式
' ============================================================
Sub ApplyShapeStyle(shp As Shape)
    With shp
        ' 添加轻微阴影
        .Shadow.Type = msoShadowOuterBottomRight
        .Shadow.Blur = 5
        .Shadow.OffsetX = 2
        .Shadow.OffsetY = 2
        .Shadow.Transparency = 0.5
        
        ' 圆角效果
        If .Type = msoShapeRectangle Then
            .Adjustments(1) = 0.1  ' 轻微圆角
        End If
    End With
End Sub

' ============================================================
' 对齐内容
' ============================================================
Sub AlignContent(slide As slide)
    Dim shp As Shape
    Dim shapesArray() As Shape
    Dim i As Integer
    Dim shapeCount As Integer
    
    shapeCount = 0
    
    ' 收集所有形状
    For Each shp In slide.Shapes
        If shp.Type = msoTextBox Or shp.Type = msoPlaceholder Then
            shapeCount = shapeCount + 1
            ReDim Preserve shapesArray(1 To shapeCount)
            Set shapesArray(shapeCount) = shp
        End If
    Next shp
    
    ' 如果有多个形状，左对齐
    If shapeCount > 1 Then
        slide.Shapes.Range.Align msoAlignLeftes, msoFalse
    End If
End Sub

' ============================================================
' 添加页脚
' ============================================================
Sub AddFooter(ppt As Presentation)
    Dim slide As slide
    Dim shp As Shape
    Dim footerText As String
    
    footerText = "龚璐 - 个人简介"
    
    For Each slide In ppt.Slides
        ' 添加页脚文本
        Set shp = slide.Shapes.AddTextbox( _
            Orientation:=msoTextOrientationHorizontal, _
            Left:=ppt.PageSetup.SlideWidth - 100, _
            Top:=ppt.PageSetup.SlideHeight - 30, _
            Width:=80, _
            Height:=20)
        
        With shp.TextFrame.TextRange
            .Text = footerText
            .Font.Size = 10
            .Font.Color.RGB = HexToColor("#9ca3af")
            .ParagraphFormat.Alignment = ppAlignRight
        End With
        
        shp.ZOrder msoSendToBack
    Next slide
End Sub

' ============================================================
' 应用过渡效果
' ============================================================
Sub ApplyTransitions(ppt As Presentation)
    Dim slide As slide
    
    For Each slide In ppt.Slides
        With slide.SlideShowTransition
            .EntryEffect = ppEffectFade
            .Duration = 0.5
            .AdvanceOnClick = msoTrue
            .AdvanceOnTime = msoFalse
        End With
    Next slide
End Sub

' ============================================================
' 辅助函数：Hex 颜色转 RGB
' ============================================================
Function HexToColor(hexColor As String) As Long
    Dim r As Integer, g As Integer, b As Integer
    
    ' 移除 # 符号
    hexColor = Replace(hexColor, "#", "")
    
    ' 转换 Hex 到 RGB
    r = Val("&H" & Mid(hexColor, 1, 2))
    g = Val("&H" & Mid(hexColor, 3, 2))
    b = Val("&H" & Mid(hexColor, 5, 2))
    
    ' 返回 RGB 颜色值
    HexToColor = RGB(r, g, b)
End Function

' ============================================================
' 附加功能：添加专业背景
' ============================================================
Sub AddProfessionalBackground()
    Dim slide As slide
    Dim shp As Shape
    
    For Each slide In ActivePresentation.Slides
        ' 添加渐变背景
        Set shp = slide.Shapes.AddShape( _
            Type:=msoShapeRectangle, _
            Left:=0, Top:=0, _
            Width:=ActivePresentation.PageSetup.SlideWidth, _
            Height:=ActivePresentation.PageSetup.SlideHeight)
        
        With shp
            .Fill.TwoColorGradient _
                Style:=msoGradientHorizontal, _
                Variant:=1
            .Fill.ForeColor.RGB = HexToColor(COLOR_BG)
            .Fill.BackColor.RGB = HexToColor(COLOR_BG_LIGHT)
            .Line.Visible = msoFalse
            .ZOrder msoSendToBack
        End With
    Next slide
    
    MsgBox "✓ 已添加专业渐变背景", vbInformation, "完成"
End Sub

' ============================================================
' 附加功能：创建时间线
' ============================================================
Sub CreateTimeline()
    Dim slide As slide
    Dim shp As Shape
    Dim i As Integer
    Dim positions As Variant
    Dim labels As Variant
    
    Set slide = ActivePresentation.Slides.Add( _
        ActivePresentation.Slides.Count + 1, _
        ppLayoutBlank)
    
    ' 添加时间线
    Set shp = slide.Shapes.AddLine( _
        BeginX:=50, BeginY:=200, _
        EndX:=ActivePresentation.PageSetup.SlideWidth - 50, EndY:=200)
    
    With shp.Line
        .ForeColor.RGB = HexToColor(COLOR_PRIMARY)
        .Weight = 3
    End With
    
    MsgBox "✓ 时间线框架已创建，请添加具体内容", vbInformation, "完成"
End Sub

' ============================================================
' 使用说明
' ============================================================
' 
' 如何运行此宏：
' 
' 1. 打开 PowerPoint
' 2. 按 Alt + F11 打开 VBA 编辑器
' 3. 插入 → 模块
' 4. 粘贴此代码
' 5. 按 F5 运行 BeautifyPresentation
' 
' 或者：
' 1. 开发工具 → 宏 → 选择 BeautifyPresentation → 运行
' 
' 注意事项：
' - 启用宏：文件 → 选项 → 信任中心 → 宏设置 → 启用所有宏
' - 备份原文件后再运行
' - 运行后可手动微调
' 
' ============================================================