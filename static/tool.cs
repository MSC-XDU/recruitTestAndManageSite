using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace WindowsFormsApplication1
{
    public partial class Form1 : Form
    {
        struct substr
        {
            public string str;
            public int num;
        }

        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            string filepath = "D:\\文本.txt";//用于统计用的文本路径
            
            sub_run(filepath, "D:\\答案\\结果2.txt", 2);
            sub_run(filepath, "D:\\答案\\结果3.txt", 3);
            sub_run(filepath, "D:\\答案\\结果4.txt", 4);
            
        }

        private void sub_run(string path,string resultpath,int n)//n 记录每次切片的一组中包含的字符数
        {
            string stxt = System.IO.File.ReadAllText(path);//语言数据读取

            //Console.WriteLine(stxt);

            substr[] tmp_str = new substr[stxt.Length - n];

            for (int i = 0; i < stxt.Length - n; i++)//文本切片，每2个字符为一组
            {
                tmp_str[i].str = stxt.Substring(i, n);
                tmp_str[i].num = 1;
            }

            for (int i = 0; i < tmp_str.Length; i++)//统计每个切片出现的次数
            {
                if (tmp_str[i].num == 0) continue;
                for (int j = tmp_str.Length - 1; j > i; j--)
                {
                    if (tmp_str[i].str == tmp_str[j].str)
                    {
                        tmp_str[i].num++;
                        tmp_str[j].num--;
                    }
                }
            }

            for (int i = 0; i < tmp_str.Length; i++)//按频数从大到小的顺序排序
            {
                for (int j = i + 1; j < tmp_str.Length; j++)
                {
                    if (tmp_str[i].num < tmp_str[j].num)
                    {
                        substr tmp = tmp_str[i];
                        tmp_str[i] = tmp_str[j];
                        tmp_str[j] = tmp;
                    }
                }
            }
            string r = "";
            for (int i = 0; i < tmp_str.Length; i++)
            {
                if(tmp_str [i].num!=0)
                {
                    r = r + tmp_str[i].str + "    " + tmp_str[i].num.ToString() + "\r\n";
                }
            }
            System.IO.File.WriteAllText(resultpath, r);

            Console.WriteLine("***文件 "+path+" 的 "+n.ToString ()+"字符切片统计 已经OK");
        }
    }
}