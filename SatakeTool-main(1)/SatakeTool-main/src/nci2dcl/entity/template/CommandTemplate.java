package nci2dcl.entity.template;

import nci2dcl.entity.nci.ProcessType;

import java.io.FileNotFoundException;
import java.io.PrintStream;
import java.util.LinkedList;
import java.util.List;
import java.util.Objects;
import java.util.Set;

public class CommandTemplate {
    private final List<CommandTemplateFragment> fragments = new LinkedList<>();

    public void addFragment(CommandTemplateFragment fragment) {
        this.fragments.add(fragment);
    }

    // For Debug
    public void toCsv() {
        try(PrintStream ps = new PrintStream("ct.csv")) {
            for(CommandTemplateFragment fragment: fragments) {
                ps.println(fragment.toCsv());
            }

        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
    }

    public List<CommandTemplateFragment> getCommandFragmentsWith(CommandTemplateFragmentType type) {
        List<CommandTemplateFragment> commandFragments = new LinkedList<>();
        for(CommandTemplateFragment fragment: fragments) {
            if(fragment.isTypeOf(type)) {
                commandFragments.add(fragment);
            }
        }
        return commandFragments;
    }

    public List<CommandTemplateFragment> getTemplateCommandFragments(String metaClassName, ProcessType processType) {
        List<CommandTemplateFragment> groupCommandFragments = new LinkedList<>();
        for(CommandTemplateFragment fragment: fragments) {
            if(fragment.isTypeOf(CommandTemplateFragmentType.TEMPLATE)
                    && Objects.equals(fragment.getSpecificationItemGroup(), metaClassName)
                    && fragment.getProcessTypes().contains(processType)) {
                groupCommandFragments.add(fragment);
            }
        }
        return groupCommandFragments;
    }
}
