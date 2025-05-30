import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public class FileExistenceCheck {

    public static void main(String[] args) {

        // 元の文字列パス
        String asisModelFilePath = ".\\VERIFICATIONforNCMonGNS3\\input\\campus_asis_axies.asta";
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
    }
}
