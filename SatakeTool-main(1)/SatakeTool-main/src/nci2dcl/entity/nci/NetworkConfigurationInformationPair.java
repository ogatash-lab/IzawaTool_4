package nci2dcl.entity.nci;

import java.io.FileNotFoundException;
import java.io.PrintStream;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;

public class NetworkConfigurationInformationPair {
    private NetworkConfigurationInformation asis;
    private NetworkConfigurationInformation tobe;

    public NetworkConfigurationInformationPair(NetworkConfigurationInformation asis, NetworkConfigurationInformation tobe) {
        this.asis = asis;
        this.tobe = tobe;
    }

    public void toCsv() {
        toCsv(asis, "asis");
        toCsv(tobe, "tobe");
    }

    private void toCsv(NetworkConfigurationInformation nci, String filename) {
        try(PrintStream ps = new PrintStream(filename + ".csv")) {
            ps.println(",,,DiffType");
            for(SpecificationItemGroup group: nci.getSpecificationItemGroups()) {
                ps.println(group.getIdentifier() + "," + group.getMetaClassName() + ",,");
                for(SpecificationItem item: group.getSpecificationItems()) {
                    ps.println("," + item.getName() + "," + item.getValue() + "," + item.getProcessType());
                }
                for(SpecificationItemGroup linked: group.getLinkedSpecificationItemGroups()) {
                    ps.println("," + linked.getIdentifier() + "," + linked.getMetaClassName());
                }
            }
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
    }

    public List<SpecificationItemGroup> getAsisConfigs() {
        return asis.getConfigs();
    }

    public List<SpecificationItemGroup> getTobeConfigs() {
        return tobe.getConfigs();
    }

    public void diff() {
        for(SpecificationItemGroup asisGroup: asis.getSpecificationItemGroups()) {
            if(tobe.hasGroupWith(asisGroup)) {
                SpecificationItemGroup correspondingTobeGroup = tobe.getGroupWith(asisGroup);
                if(asisGroup.isSameAs(correspondingTobeGroup)) {
                    asisGroup.tag(ProcessType.NO_CHANGE);
                    correspondingTobeGroup.tag(ProcessType.NO_CHANGE);
                } else {
                    SpecificationItemGroup.diff(asisGroup, correspondingTobeGroup);
                }
            } else {
                asisGroup.tagWithoutEmptyValue(ProcessType.UNSET);
            }
        }

        for(SpecificationItemGroup tobeGroup: tobe.getSpecificationItemGroups()) {
            if(!asis.hasGroupWith(tobeGroup)) {
                tobeGroup.tagWithoutEmptyValue(ProcessType.SET);
            }
        }

    }

    //LinkedHashSetとしてる -> 重複を許さない
    //許してしまうとcf1 cf1 cf2となる
    public Set<String> getConfigIdentifiers() {
        Set<String> configIdentifiers = new LinkedHashSet<>();
        for (SpecificationItemGroup asisConfig : getAsisConfigs()) {
            configIdentifiers.add(asisConfig.getIdentifier());
        }
        for (SpecificationItemGroup tobeConfig : getTobeConfigs()) {
            configIdentifiers.add(tobeConfig.getIdentifier());
        }
            //System.out.println(configIdentifiers);
        return  configIdentifiers;
    }
}
