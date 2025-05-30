package nci2dcl.control;

import nci2dcl.entity.nci.NetworkConfigurationInformation;
import nci2dcl.entity.nci.NetworkConfigurationInformationPair;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public class DifferenceDetector {
    public static NetworkConfigurationInformationPair detectDifference(String asisModelFilePath, String tobeModelFilePath) {
        NetworkConfigurationInformation asis = M2NciConverter.convert(asisModelFilePath);
        NetworkConfigurationInformation tobe = M2NciConverter.convert(tobeModelFilePath);
        // 追加
        Path p = Paths.get(".\\VERIFICATIONforNCMonGNS3\\verification-tool\\NetworkConfiguration\\NetworkConfigurationInformation.txt");
        try{
            Files.createFile(p);
        }catch(IOException e){
            System.out.println(e);
        }
        //
        try{
            File file = new File(".\\VERIFICATIONforNCMonGNS3\\verification-tool\\NetworkConfiguration\\NetworkConfigurationInformation.txt");
            FileWriter filewriter = new FileWriter(file);

            for (int i=0; i<tobe.getSpecificationItemGroups().size(); ++i)
            {
                filewriter.write(tobe.getSpecificationItemGroups().get(i).getIdentifier());
                filewriter.write("\r\n");
                for (int j=0; j<tobe.getSpecificationItemGroups().get(i).getSpecificationItems().size(); ++j){
                    filewriter.write(tobe.getSpecificationItemGroups().get(i).getSpecificationItems().get(j).getName());
                    filewriter.write("\r\n");
                    filewriter.write(tobe.getSpecificationItemGroups().get(i).getSpecificationItems().get(j).getValue());
                    filewriter.write("\r\n");
                }
                filewriter.write("-----------------------------------\r\n");
            }
            filewriter.close();
        } catch(IOException e){
            System.out.println(e);
        }
        NetworkConfigurationInformationPair pair = diff(asis, tobe);
        return pair;
    }

    private static NetworkConfigurationInformationPair diff(NetworkConfigurationInformation asis, NetworkConfigurationInformation tobe) {
        NetworkConfigurationInformationPair pair = new NetworkConfigurationInformationPair(asis, tobe);
        pair.diff();
        return pair;
    }

}
