// nci2dclパッケージの定義
package nci2dcl;

// 必要なクラスのインポート
import nci2dcl.control.CommandTailor;
import nci2dcl.control.CommandTemplateParser;
import nci2dcl.control.DifferenceDetector;
import nci2dcl.entity.command.CommandLists;
import nci2dcl.entity.template.CommandTemplate;
import nci2dcl.entity.command.CommandList;
import nci2dcl.entity.nci.NetworkConfigurationInformationPair;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import java.util.Map;

import java.nio.file.*;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

// メインクラスの定義
public class



Main_test {
    public static void
    main(String[] args){
        // プログラム開始時刻の記録
        long startTime = System.currentTimeMillis();

        String asisModelFilePath = ".\\VERIFICATIONforNCMonGNS3\\input\\campus_asis_axies.asta";

        String commandTemplateFilePath = ".\\VERIFICATIONforNCMonGNS3\\input\\cmd_cisco3725ESW.csv";


        //String tobeModelFilePath = ".\\VERIFICATIONforNCMonGNS3\\input\\campus_tobe_axies_withCf4Cf6NotOSPF.asta";

        //結線なし
        //String tobeModelFilePath = ".\\VERIFICATIONforNCMonGNS3\\input\\campus_tobe_axies_withCf4NotOSPF.asta";

        //２－６結線
        String tobeModelFilePath = ".\\VERIFICATIONforNCMonGNS3\\input\\campus_tobe_axies_withCf4NotOSPF_izawa.asta";

        // Path オブジェクトへ変換（ OS 依存文字を自動調整 ）
        Path asis = Paths.get(asisModelFilePath).normalize();
        Path tobe = Paths.get(tobeModelFilePath).normalize();

        // 存在確認
        boolean asisExists = Files.exists(asis);
        boolean tobeExists = Files.exists(tobe);

        // 結果表示
        if (asisExists) {
            System.out.println("[OK] AS-IS ファイル発見: " + asis.toAbsolutePath());
        } else {
            System.err.println("[NG] AS-IS ファイルが見つかりません: " + asis.toAbsolutePath());
        }

        if (tobeExists) {
            System.out.println("[OK] TO-BE ファイル発見: " + tobe.toAbsolutePath());
        } else {
            System.err.println("[NG] TO-BE ファイルが見つかりません: " + tobe.toAbsolutePath());
        }

        // どちらか一方でも欠けていたら、適宜例外を投げるなど
        if (!asisExists || !tobeExists) {
            throw new IllegalStateException("必要な .asta ファイルが不足しています。パスを確認してください。");
        }

        // 設定変更検出の実行
        NetworkConfigurationInformationPair nciPair = DifferenceDetector.detectDifference(asisModelFilePath, tobeModelFilePath);
        nciPair.toCsv();  // 差分情報をCSVファイルに出力
        CommandTemplate template = CommandTemplateParser.parse(commandTemplateFilePath); // コマンドテンプレートの解析
        template.toCsv();  // テンプレート情報をCSVファイルに出力
        CommandLists commandLists = CommandTailor.tailor(nciPair, template); // コマンドリストの生成

        // 生成されたコマンドリストの保存
        for(Map.Entry<String, CommandList> entry: commandLists.getConfigCommandListMap().entrySet()){

            //cmd_kiki_cf1~9の生成
            Path p = Paths.get(".\\VERIFICATIONforNCMonGNS3\\verification-tool\\cmd_node\\cmd_kiki\\cmd_kiki_" + entry.getKey() + ".txt");

        }

        //追加箇所2024-9-19 ディレクトリ名取得
        Path path = Paths.get(".\\VERIFICATIONforNCMonGNS3\\verification-tool\\cmd_node");

        // ディレクトリ名を保存するリスト
        List<String> directoryNames = new ArrayList<>();

        try (DirectoryStream<Path> stream = Files.newDirectoryStream(path)) {
            for (Path entry : stream) {
                // ディレクトリのみをリストに追加
                if (Files.isDirectory(entry)) {
                    directoryNames.add(entry.getFileName().toString());
                }
            }
        } catch (IOException | DirectoryIteratorException e) {
            System.err.println("エラーが発生しました: " + e);
        }


        // ディレクトリ名の配列に変換し、表示
        String[] directoriesArray = directoryNames.toArray(new String[0]);
        System.out.println("ディレクトリ一覧:");
        for

        (String name : directoriesArray) {
            System.out.println(name);

            String fileName = "folder_name.txt";
            try {
                Path currentPath = Paths.get(".\\VERIFICATIONforNCMonGNS3\\verification-tool\\20231115");
                Path filePath = currentPath.resolve(fileName);

                // ファイルに書き込み前に内容をクリア
                Files.writeString(filePath, name, StandardOpenOption.CREATE, StandardOpenOption.TRUNCATE_EXISTING);
                System.out.println("ファイルが正常に書き込まれました: " + filePath);
            } catch (IOException e) {
                System.err.println("ファイルの書き込みに失敗しま" +
                        "した: " + e.getMessage());
            }

            // Pythonプログラムの実行を専用メソッドで行う
            runPythonScript();

            // ネットワークをクリアする
            nodeDelete();




            System.out.println("~~~~~~~~~~~~~~~~~~" + name + "~~~~~~~~~~~~~~~~~~~~");
        }

        // ... [残りのコード]




        long endTime = System.currentTimeMillis(); // プログラム終了時刻の記録

        // 開始時刻、終了時刻、実行時間の出力
        System.out.println("開始時刻：" + startTime + " ms");
        System.out.println("終了時刻：" + endTime + " ms");
        System.out.println("処理時間：" + (endTime - startTime)/1000 + " s");
    }



    // Pythonスクリプトを実行するためのメソッド
    public static void runPythonScript() {
        try {
            String command = "cmd.exe /c python VERIFICATIONforNCMonGNS3/verification-tool/20231115/main.py";
            Process p = Runtime.getRuntime().exec(command);


            // 子プロセスの標準出力および標準エラー出力を処理
            StreamThread outputThread = new StreamThread(p.getInputStream(), System.out);
            outputThread.start();
            StreamThread errorThread = new StreamThread(p.getErrorStream(), System.err);
            errorThread.start();

            // プロセスの終了を待機
            int exitCode = p.waitFor();
            System.out.println("Pythonスクリプトの終了コード: " + exitCode);

            // スレッドの終了を待機


            outputThread.join();
            errorThread.join();

            p.destroy(); // プロセスの破棄

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void nodeDelete() {
        try {

            String command = "cmd.exe /c python VERIFICATIONforNCMonGNS3/verification-tool/20231115/node_delete.py";
            Process p = Runtime.getRuntime().exec(command);

            // 子プロセスの標準出力および標準エラー出力を処理
            StreamThread outputThread = new StreamThread(p.getInputStream(), System.out);
            outputThread.start();
            StreamThread errorThread = new StreamThread(p.getErrorStream(), System.err);
            errorThread.start();


            // プロセスの終了を待機
            int exitCode = p.waitFor();
            System.out.println("Pythonスクリプトの終了コード: " + exitCode);

            // スレッドの終了を待機
            outputThread.join();
            errorThread.join();

            p.destroy(); // プロセスの破棄

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    // 入出力ストリームを扱うためのスレッドクラス
    static class StreamThread extends Thread {
        private InputStream in;

        private OutputStream out;

        public StreamThread(InputStream in, OutputStream out) {
            this.in = in;
            this.out = out;
        }


        public void run() {
            try {
                byte[] buffer = new byte[4096];
                int length;
                while ((length = in.read(buffer)) != -1) {
                    out.write(buffer, 0, length);
                    out.flush(); // バッファを強制的にフラッシュ
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

    }
}