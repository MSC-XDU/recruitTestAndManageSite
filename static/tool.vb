Public Class Form1
    Structure substr
        Public str As String
        Public num As Integer
    End Structure
    Private Sub Form1_Load(sender As Object, e As EventArgs) Handles MyBase.Load
        Dim filepath As String = "D:\文本.txt"    '用于统计用的文本路径
        sub_run(filepath, "D:\答案\结果2.txt", 2)
        sub_run(filepath, "D:\答案\结果3.txt", 3)
        sub_run(filepath, "D:\答案\结果4.txt", 4)
    End Sub
    Private Sub sub_run(path As String, resultpath As String, n As Integer)
        REM    n 记录每次切片的一组中包含的字符数

        Dim stxt As String = System.IO.File.ReadAllText(path)    '语言数据读取

        'Console.WriteLine(stxt)

        Dim tmp_str(stxt.Length - n) As substr

        For i = 0 To stxt.Length - n - 1    '文本切片，每2个字符为一组
            tmp_str(i).str = stxt.Substring(i, n)
            tmp_str(i).num = 1
        Next
        For i = 0 To tmp_str.Length - 1    '统计每个切片出现的次数
            If (tmp_str(i).num = 0) Then Continue For
            For j = tmp_str.Length - 1 To i + 1 Step -1
                If (tmp_str(i).str = tmp_str(j).str) Then
                    tmp_str(i).num += 1
                    tmp_str(j).num -= 1
                End If
            Next
        Next

        For i = 0 To tmp_str.Length - 1    '按频数从大到小的顺序排序
            For j = i + 1 To tmp_str.Length - 1
                If (tmp_str(i).num < tmp_str(j).num) Then
                    Dim tmp As substr = tmp_str(i)
                    tmp_str(i) = tmp_str(j)
                    tmp_str(j) = tmp
                End If
            Next
        Next

        Dim r As String = ""
        For i = 0 To tmp_str.Length - 1
            If (tmp_str(i).num <> 0) Then
                r = r & tmp_str(i).str & "    " & tmp_str(i).num.ToString() + vbCrLf
            End If
        Next
        System.IO.File.WriteAllText(resultpath, r)

        Console.WriteLine("***文件 " + path + " 的 " + n.ToString() + "字符切片统计 已经OK")
    End Sub
End Class