package nci2dcl.control;

import nci2dcl.entity.command.Command;
import nci2dcl.entity.command.CommandList;
import nci2dcl.entity.command.CommandLists;
import nci2dcl.entity.nci.ProcessType;
import nci2dcl.entity.nci.NetworkConfigurationInformationPair;
import nci2dcl.entity.nci.SpecificationItemGroup;
import nci2dcl.entity.template.CommandTemplate;
import nci2dcl.entity.template.CommandTemplateFragment;
import nci2dcl.entity.template.CommandTemplateFragmentType;

import java.util.*;

public class CommandTailor {
    private static final List<String> stopSearchMetaClassNames = new LinkedList(Arrays.asList("link"));

    public static CommandLists tailor(NetworkConfigurationInformationPair nciPair, CommandTemplate template) {
        CommandLists commandLists = new CommandLists();
        for(String configIdentifier: nciPair.getConfigIdentifiers()){
            CommandList commandList = new CommandList();

            commandLists.put(configIdentifier, commandList);

            //ヘッダー
            parseSimpleCommand(commandList, template.getCommandFragmentsWith(CommandTemplateFragmentType.HEADER));

            //設定解除（unset）
            for (SpecificationItemGroup asisConfig : nciPair.getAsisConfigs()) {
                if(Objects.equals(configIdentifier, asisConfig.getIdentifier())){
                    exploreCommands(commandList, asisConfig, template, ProcessType.UNSET);
                }
            }

            //設定do（set）
            for (SpecificationItemGroup tobeConfig : nciPair.getTobeConfigs()) {
                if(Objects.equals(configIdentifier, tobeConfig.getIdentifier())){
                    exploreCommands(commandList, tobeConfig, template, ProcessType.SET);
                }
            }

            //フッター
            parseSimpleCommand(commandList, template.getCommandFragmentsWith(CommandTemplateFragmentType.FOOTER));

            //階層に入るか入らないかの判定
            exploreModeCommands(commandList, template.getCommandFragmentsWith(CommandTemplateFragmentType.MODE_BEFORE), template.getCommandFragmentsWith(CommandTemplateFragmentType.MODE_AFTER));
        }

        return commandLists;
    }

    private static void parseSimpleCommand(CommandList commandList, List<CommandTemplateFragment> commandTemplateFragments) {
        for(CommandTemplateFragment fragment: commandTemplateFragments) {
            if(commandList.existDependentCommand(fragment.getDependentCommandId())) {
                commandList.addCommand(new Command(fragment.getRawCommand(), ProcessType.NO_CHECK, fragment));
            }
        }
    }

    private static void exploreCommands(CommandList commandList, SpecificationItemGroup config, CommandTemplate template, ProcessType processType) {
        exploreCommands(commandList, config, template, processType, new HashSet<>());
    }

    private static void exploreCommands(CommandList commandList, SpecificationItemGroup group, CommandTemplate template, ProcessType processType, Set<SpecificationItemGroup> processed) {
        // process template commands
        List<CommandTemplateFragment> groupFragments = template.getTemplateCommandFragments(group.getMetaClassName(), processType);
        for(CommandTemplateFragment fragment: groupFragments) {
            if(commandList.existDependentCommand(fragment.getDependentCommandId())
                    && (fragment.match(group, processType) || fragment.isModal())) {
                commandList.addCommand(new Command(fragment.getCommand().embody(group), fragment.getCommand().identifyProcessType(group), fragment));
            }
        }

        // tag the group as processed
        processed.add(group);

        // search linked groups
        for(SpecificationItemGroup linked: group.getLinkedSpecificationItemGroups()) {
            if(stopSearchMetaClassNames.contains(linked.getMetaClassName().toLowerCase())
                    || processed.contains(linked)) {
                continue;
            }
            exploreCommands(commandList, linked, template, processType, processed);
        }
    }

    private static void exploreModeCommands(CommandList commandList, List<CommandTemplateFragment> beforeFragments, List<CommandTemplateFragment> afterFragments) {
        commandList.removeUnnecessaryModalCommand();
        exploreModeCommands(commandList.getStructuredCommands(), beforeFragments, afterFragments);
        commandList.regenerateSequentialList();
    }

    private static void exploreModeCommands(List<Command> followingCommands, List<CommandTemplateFragment> beforeFragments, List<CommandTemplateFragment> afterFragments) {
        Stack<Integer> stack = new Stack();
        for (int i = 0; i < followingCommands.size(); i++) {
            Command command = followingCommands.get(i);
            if(command.isModal()) {
                stack.push(i);
            }
            if(!command.getFollowingCommands().isEmpty()) {
                exploreModeCommands(command.getFollowingCommands(), beforeFragments, afterFragments);
            }
        }

        while(!stack.empty()) {
            int insertNum = stack.peek() + 1;

            List<Command> modeAfterCommands = getCommandsFromFragments(afterFragments);
            followingCommands.addAll(insertNum, modeAfterCommands);

            insertNum = stack.pop();

            List<Command> modeBeforeCommands = getCommandsFromFragments(beforeFragments);
            followingCommands.addAll(insertNum, modeBeforeCommands);
        }
    }

    private static List<Command> getCommandsFromFragments(List<CommandTemplateFragment> commandTemplateFragments) {
        List<Command> commands = new LinkedList<>();
        ListIterator<CommandTemplateFragment> commandTemplateFragmentListIterator = commandTemplateFragments.listIterator(commandTemplateFragments.size());
        while (commandTemplateFragmentListIterator.hasPrevious()) {
            CommandTemplateFragment fragment = commandTemplateFragmentListIterator.previous();
            commands.add(new Command(fragment.getRawCommand(), ProcessType.NO_CHECK, fragment));
        }
        return commands;
    }
}
