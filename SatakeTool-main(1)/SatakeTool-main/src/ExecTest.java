import java.io.*;

public class ExecTest {
    public static void main(String[] args) throws Exception {
        new ExecTest();
    }

    public ExecTest() throws Exception {
        // "sort data.txt"を、子プロセスとして実行
        // sortは、テキストをソートするコマンド
        // data.txtは、javaプロセスのカレントディレクトリ上のテキストファイル
        Process p = Runtime.getRuntime().exec("python verification-tool/tool.py");

        // 子プロセスの標準出力および標準エラー出力を入力するスレッドを起動
        new StreamThread(p.getInputStream()).start();

        p.waitFor();  // 子プロセスの終了を待つ
        p.destroy();  // 子プロセスの明示的に終了させ、資源を回収できるようにする
    }

    /**
     *子プロセスの出力ストリームから入力し、ファイルに出力するスレッド
     */
    class StreamThread extends Thread {
        private static final int BUF_SIZE = 4096;
        private InputStream in;
        private OutputStream out;

        public StreamThread(InputStream in) throws IOException {
            this.in  = in;
            this.out = System.out;
        }

        public void run(){
            byte[] buf = new byte[BUF_SIZE];
            int size = -1;
            try{
                while((size = in.read(buf, 0, BUF_SIZE)) != -1){
                    out.write(buf, 0, size);
                }
            }catch(IOException ex){
                ex.printStackTrace();
            }finally{
                try{in.close();} catch(IOException ex){}
                try{out.close();}catch(IOException ex){}
            }
        }
    }
}
