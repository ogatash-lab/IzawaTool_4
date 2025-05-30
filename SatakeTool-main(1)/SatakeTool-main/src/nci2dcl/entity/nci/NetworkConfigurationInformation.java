package nci2dcl.entity.nci;

import java.util.LinkedList;
import java.util.List;
import java.util.Objects;

public class NetworkConfigurationInformation {
    private final static String ROOT_NAME1 = "config";
    private final static String ROOT_NAME2 = "client";
    private List<SpecificationItemGroup> specificationItemGroups = new LinkedList<>();

    public List<SpecificationItemGroup> getSpecificationItemGroups() {
        return this.specificationItemGroups;
    }

    public void addGroup(SpecificationItemGroup group) {
        this.specificationItemGroups.add(group);
    }

    public boolean hasGroupWith(SpecificationItemGroup inputGroup) {
        for(SpecificationItemGroup group: specificationItemGroups) {
            if(Objects.equals(group.getIdentifier(), inputGroup.getIdentifier())
                    && Objects.equals(group.getMetaClassName(), inputGroup.getMetaClassName())) {
                return true;
            }
        }
        return false;
    }

    public SpecificationItemGroup getGroupWith(SpecificationItemGroup inputGroup) {
        for(SpecificationItemGroup group: specificationItemGroups) {
            if(Objects.equals(group.getIdentifier(), inputGroup.getIdentifier())
                    && Objects.equals(group.getMetaClassName(), inputGroup.getMetaClassName())) {
                return group;
            }
        }
        return null;
    }

    public List<SpecificationItemGroup> getConfigs() {
        List<SpecificationItemGroup> configs = new LinkedList<>();
        for(SpecificationItemGroup group: this.specificationItemGroups) {
            if(Objects.equals(ROOT_NAME1, group.getMetaClassName().toLowerCase())) {
                configs.add(group);
            }
        }
        return configs;
    }

    // GNS3のvpcs用
    public List<SpecificationItemGroup> getClients() {
        List<SpecificationItemGroup> clients = new LinkedList<>();
        for(SpecificationItemGroup group: this.specificationItemGroups) {
            if(Objects.equals(ROOT_NAME2, group.getMetaClassName().toLowerCase())) {
                clients.add(group);
            }
        }
        return clients;
    }
}
