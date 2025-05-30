package nci2dcl.entity.template;

import nci2dcl.entity.nci.ProcessType;
import nci2dcl.entity.nci.SpecificationItem;
import nci2dcl.entity.nci.SpecificationItemGroup;

import java.util.LinkedList;
import java.util.List;
import java.util.Objects;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class AbstractCommand {
    private static final Pattern commandPattern = Pattern.compile(".*?(<.+?>)*.*?");

    private String command = "";
    private List<String> parameters = new LinkedList<>();

    public AbstractCommand(String command) {
        this.command = command;

        Matcher m = commandPattern.matcher(command);
        while(m.find()) {
            for (int i = 0; i < m.groupCount(); i++) {
                String group = m.group(i).trim();
                if(isParameter(group)) {
                    parameters.add(group);
                }
            }
        }
    }

    private boolean isParameter(String string) {
        return string.startsWith("<") && string.endsWith(">");
    }

    @Override
    public String toString() {
        return this.command;
    }

    public String getRawCommand() {
        return this.command;
    }

    public boolean match(SpecificationItemGroup group) {
        for(String parameter: parameters) {
            SpecificationItem item = group.searchItem(deParameterize(parameter));
            if(item == null || item.getValue().isEmpty()) {
                return false;
            }
        }
        return true;
    }

    private String parametrize(String name) {
        return "<" + name + ">";
    }

    public String embody(SpecificationItemGroup group) {
        String embodied = this.command;
        for(String parameter: this.parameters) {
            SpecificationItem item = group.searchItem(deParameterize(parameter));
            if(item != null && Objects.equals(parameter, parametrize(item.getName()))) {
                embodied = embodied.replace(parameter, item.getValue());
            }
        }
        return embodied;
    }

    private String deParameterize(String parameter) {
        return parameter.replaceAll("[<>]", "");
    }

    public ProcessType identifyProcessType(SpecificationItemGroup group) {
        for(String parameter: this.parameters) {
            SpecificationItem item = group.searchItem(deParameterize(parameter));
            if(item != null && Objects.equals(parameter, parametrize(item.getName()))) {
                return item.getProcessType();
            }
        }
        return ProcessType.NO_CHANGE;
    }
}
