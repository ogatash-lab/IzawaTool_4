package nci2dcl.entity.command;

import nci2dcl.entity.nci.ProcessType;

import java.util.LinkedList;
import java.util.List;
import java.util.ListIterator;

public class CommandList {
    private List<Command> sequentialCommands = new LinkedList<>();
    private List<Command> structuredCommands = new LinkedList<>();

    public void addCommand(Command addingCommand) {
        ListIterator<Command> commandIterator = sequentialCommands.listIterator(sequentialCommands.size());
        while (commandIterator.hasPrevious()) {
            Command existingCommand = commandIterator.previous();
            if(existingCommand.getId() == addingCommand.getDependentCommandId()) {
                existingCommand.addFollowingCommands(addingCommand);
                addingCommand.setPrerequisiteCommand(existingCommand);
                break;
            }
        }
        this.sequentialCommands.add(addingCommand);
        if(addingCommand.getPrerequisiteCommand() == null) {
            structuredCommands.add(addingCommand);
        }
    }

    public boolean existDependentCommand(int dependentCommandId) {
        if(dependentCommandId < 0) {
            return true;
        }

        for(Command command: sequentialCommands) {
            if(command.getId() == dependentCommandId) {
                return true;
            }
        }

        return false;
    }

    public List<Command> getSequentialCommands() {
        return this.sequentialCommands;
    }

    public List<Command> getStructuredCommands() {
        return structuredCommands;
    }

    public void removeUnnecessaryModalCommand() {
        removeUnnecessaryModalCommand(structuredCommands);
    }

    private void removeUnnecessaryModalCommand(List<Command> commands) {
        List<Command> removals = new LinkedList<>();
        for(Command command: commands) {
            if(command.isModal()
                    && command.getFollowingCommands().size() == 0
                    && command.getProcessType() == ProcessType.NO_CHANGE) {
                removals.add(command);
            }
            removeUnnecessaryModalCommand(command.getFollowingCommands());
        }
        commands.removeAll(removals);
    }

    public void regenerateSequentialList() {
        this.sequentialCommands.clear();
        regenerateSequentialList(structuredCommands);
    }

    private void regenerateSequentialList(List<Command> commands) {
            for(Command command: commands) {
                this.sequentialCommands.add(command);
                regenerateSequentialList(command.getFollowingCommands());
            }
    }

}
