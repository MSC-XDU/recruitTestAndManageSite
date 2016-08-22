import java.io.*;

class substr{
	public String str;
	public int num;
}

public class tool{
	public static void main(String[] args){
		String filepath = "D:\\�ı�.txt";//����ͳ���õ��ı�·��
        sub_run(filepath, "D:\\��\\���2.txt", 2);
        sub_run(filepath, "D:\\��\\���3.txt", 3);
        sub_run(filepath, "D:\\��\\���4.txt", 4);
	}
	public static void sub_run(String path,String resultpath,int n){//n ��¼ÿ����Ƭ��һ���а������ַ���
		String stxt="";
		try{
			File fin=new File(path);
			int len=(int)fin.length();
			byte btxt[]=new byte[len];
			if(fin.exists()){
				RandomAccessFile f = new RandomAccessFile(fin,"rw");
				f.read(btxt,0,len);
				stxt=new String(btxt,"utf-8");
				f.close();
			}
		}
		catch(IOException e){
			e.printStackTrace();
		}
		
		substr tmp_str[] = new substr[stxt.length() - n];
		
		for (int i = 0; i < stxt.length() - n; i++)//�ı���Ƭ��ÿ2���ַ�Ϊһ��
        {
			tmp_str[i]=new substr();
			tmp_str[i].str = stxt.substring(i, i+n);
            tmp_str[i].num = 1;
        }
		for (int i = 0; i < tmp_str.length; i++)//ͳ��ÿ����Ƭ���ֵĴ���
        {
            if (tmp_str[i].num == 0) continue;
            for (int j = tmp_str.length - 1; j > i; j--)
            {
                if (tmp_str[i].str.equals(tmp_str[j].str))
                {
                    tmp_str[i].num++;
                    tmp_str[j].num--;
                }
            }
        }
		for (int i = 0; i < tmp_str.length; i++)//��Ƶ���Ӵ�С��˳������
        {
            for (int j = i + 1; j < tmp_str.length; j++)
            {
                if (tmp_str[i].num < tmp_str[j].num)
                {
                    substr tmp = tmp_str[i];
                    tmp_str[i] = tmp_str[j];
                    tmp_str[j] = tmp;
                }
            }
        }
		String r = "";
		for (int i = 0; i < tmp_str.length; i++)
        {
            if(tmp_str [i].num!=0)
            {
                r = r + tmp_str[i].str + "    " + Integer.toString(tmp_str[i].num) + "\r\n";
            }
        }
		
		try{
			File fout=new File(resultpath);
			RandomAccessFile f2=new RandomAccessFile(fout,"rw");
			f2.write(r.getBytes("utf-8"));
			f2.close();
		}
		catch(IOException e){
			e.printStackTrace();
		}
	}
}