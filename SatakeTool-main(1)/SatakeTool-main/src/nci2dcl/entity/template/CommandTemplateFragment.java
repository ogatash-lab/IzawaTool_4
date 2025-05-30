package nci2dcl.entity.template;

import nci2dcl.entity.nci.ProcessType;
import nci2dcl.entity.nci.SpecificationItem;
import nci2dcl.entity.nci.SpecificationItemGroup;

import java.util.*;

public class CommandTemplateFragment {
    private static final String SEPARATOR = "/";
    private static final String ALL_ITEMS = "*";
    private CommandTemplateFragmentType commandType = CommandTemplateFragmentType.NO_PROCESS;
    private String specificationItemGroup = ""; // Only the commands of the TEMPLATE type have concrete values
    private Set<String> specificationItems = new HashSet<>(); // Only the commands of the TEMPLATE type have concrete values
    private Set<ProcessType> processTypes = new HashSet<>();  // Only the commands of the TEMPLATE type have concrete values
    private int commandId = -1; // -1 means no id.
    private AbstractCommand command = new AbstractCommand("");
    private boolean modal = false;
    private int dependentCommandId = -1; // -1 means no value;
    private AbstractCondition condition = new AbstractCondition("");

    public CommandTemplateFragment setCommandType(String commandType) {
        this.commandType = CommandTemplateFragmentType.parse(commandType);
        return this;
    }

    public CommandTemplateFragment setSpecificationItemGroup(String specificationItemGroup) {
        this.specificationItemGroup = specificationItemGroup;
        return this;
    }

    public CommandTemplateFragment setSpecificationItems(String specificationItems) {
        for(String specificationItem: specificationItems.trim().split(SEPARATOR)) {
            this.specificationItems.add(specificationItem);
        }
        return this;
    }

    public CommandTemplateFragment setProcessTypes(String processTypes) {
        for(String processType: processTypes.trim().split(SEPARATOR)) {
            this.processTypes.add(ProcessType.parse(processType));
        }
        return this;
    }

    public CommandTemplateFragment setCommandId(String commandId) {
        try {
            this.commandId = Integer.parseInt(commandId);
        } catch (NumberFormatException e) {
        }
        return this;
    }

    public CommandTemplateFragment setCommand(String command) {
        this.command = new AbstractCommand(command.trim());
        return this;
    }

    public CommandTemplateFragment setModal(String modal) {
        this.modal = Boolean.parseBoolean(modal);
        return this;
    }

    public CommandTemplateFragment setDependentCommandId(String dependentCommandId) {
        try {
            this.dependentCommandId = Integer.parseInt(dependentCommandId);
        } catch (NumberFormatException e) {
        }
        return this;
    }

    public CommandTemplateFragment setCondition(String condition) {
        this.condition = new AbstractCondition(condition.trim());
        return this;
    }

    public String toCsv() {
        return commandType.toString()
                + "," + specificationItemGroup
                + "," + String.join(SEPARATOR, specificationItems)
                + "," + getString(processTypes)
                + "," + commandId
                + "," + command
                + "," + modal
                + "," + dependentCommandId
                + "," + condition;


    }

    private String getString(Set<ProcessType> differenceTypes) {
        StringBuilder builder = new StringBuilder();
        for (ProcessType type : differenceTypes) {
            if (!builder.toString().isEmpty()) {
                builder.append(SEPARATOR);
            }
            builder.append(type.toString());
        }
        return builder.toString();
    }

    public boolean isTypeOf(CommandTemplateFragmentType type) {
        return this.commandType == type;
    }

    public String getRawCommand() {
        return this.command.getRawCommand();
    }

    public int getCommandId() {
        return this.commandId;
    }

    public int getDependentCommandId() {
        return this.dependentCommandId;
    }

    public String getSpecificationItemGroup() {
        return specificationItemGroup;
    }

    public Set<ProcessType> getProcessTypes() {
        return processTypes;
    }

    public AbstractCommand getCommand() {
        return command;
    }

    public boolean isModal() {
        return modal;
    }

    public boolean match(SpecificationItemGroup group, ProcessType processType) {
        return this.matchItem(group, processType) && this.matchCommand(group) && this.matchCondition(group);
    }

    private boolean matchItem(SpecificationItemGroup group, ProcessType processType) {
        for(String specificationItem: specificationItems) {
            if(Objects.equals(ALL_ITEMS, specificationItem)) {
                for(SpecificationItem item: group.getSpecificationItems()) {
                    if (item.getProcessType() == processType) {
                        return true;
                    }
                }
                return false;
            }
        }

        for(String specificationItem: specificationItems) {
            SpecificationItem item = group.searchItem(specificationItem);
            if (item.getProcessType() == processType) {
                return true;
            }
        }
        return false;
    }

    private boolean matchCommand(SpecificationItemGroup group) {
        return this.command.match(group);
    }

    public boolean matchCondition(SpecificationItemGroup group) {
        return this.condition.match(group);
    }
}
