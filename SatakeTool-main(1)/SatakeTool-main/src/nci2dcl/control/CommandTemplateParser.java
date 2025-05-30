package nci2dcl.control;

import nci2dcl.entity.template.CommandTemplate;
import nci2dcl.entity.template.CommandTemplateFragment;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.util.List;

public class CommandTemplateParser {
    private static final int COLUMN_NUM = 9;

    public static CommandTemplate parse(String commandTemplateFilePath) {
        CommandTemplate commandTemplate = new CommandTemplate();
        try {
            List<String> lines = Files.readAllLines(new File(commandTemplateFilePath).toPath());
            lines.remove(0); // skip header row
            for(String line: lines) {
                String[] split = line.split(",", COLUMN_NUM);
                if(split.length < COLUMN_NUM) { // skip invalid row
                    continue;
                }

                CommandTemplateFragment fragment = new CommandTemplateFragment();
                fragment.setCommandType(split[0])
                        .setSpecificationItemGroup(split[1])
                        .setSpecificationItems(split[2])
                        .setProcessTypes(split[3])
                        .setCommandId(split[4])
                        .setCommand(split[5])
                        .setModal(split[6])
                        .setDependentCommandId(split[7])
                        .setCondition(split[8]);
                commandTemplate.addFragment(fragment);
            }

        } catch (IOException e) {
            e.printStackTrace();
        }
        return commandTemplate;
    }
}
