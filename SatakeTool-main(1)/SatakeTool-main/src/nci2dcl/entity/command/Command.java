package nci2dcl.entity.command;

import nci2dcl.entity.nci.ProcessType;
import nci2dcl.entity.template.CommandTemplateFragment;

import java.util.LinkedList;
import java.util.List;

public class Command {
    private String text;
    private ProcessType processType;
    private CommandTemplateFragment sourceFragment;

    private List<Command> followingCommands = new LinkedList<>();
    private Command prerequisiteCommand;

    public Command(String command, ProcessType processType, CommandTemplateFragment sourceFragment) {
        this.text = command;
        this.processType = processType;
        this.sourceFragment = sourceFragment;
    }

    public int getId() {
        return sourceFragment.getCommandId();
    }

    public int getDependentCommandId() {
        return sourceFragment.getDependentCommandId();
    }

    public boolean isModal() {
        return sourceFragment.isModal();
    }

    public List<Command> getFollowingCommands() {
        return followingCommands;
    }

    public void addFollowingCommands(Command followingCommands) {
        this.followingCommands.add(followingCommands);
    }

    public Command getPrerequisiteCommand() {
        return prerequisiteCommand;
    }

    public void setPrerequisiteCommand(Command prerequisiteCommand) {
        this.prerequisiteCommand = prerequisiteCommand;
    }

    public String getText() {
        return text;
    }

    public ProcessType getProcessType() { return this.processType; }
}
