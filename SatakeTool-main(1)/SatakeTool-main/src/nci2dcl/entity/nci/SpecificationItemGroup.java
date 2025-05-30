package nci2dcl.entity.nci;

import java.util.LinkedList;
import java.util.List;
import java.util.Objects;

public class SpecificationItemGroup {
    private String identifier;
    private String metaClassName; // TODO: Create the structure of this object;
    private List<SpecificationItemGroup> linkedSpecificationItemGroups = new LinkedList<>();
    private List<SpecificationItem> specificationItems = new LinkedList<>();

    public SpecificationItemGroup(String identifier, String metaClassName) {
        this.identifier = identifier;
        this.metaClassName = metaClassName;
    }

    public static void diff(SpecificationItemGroup asisGroup, SpecificationItemGroup tobeGroup) {
        next: for(SpecificationItem tobeItem: tobeGroup.specificationItems) {
            for(SpecificationItem asisItem: asisGroup.specificationItems) {
                if(Objects.equals(tobeItem.getName(), asisItem.getName())) {
                    if(Objects.equals(tobeItem.getValue(), asisItem.getValue())) {
                        tobeItem.tag(ProcessType.NO_CHANGE);
                        asisItem.tag(ProcessType.NO_CHANGE);
                    } else {
                        if (!tobeItem.getValue().isEmpty()) {
                            tobeItem.tag(ProcessType.SET);
                        } else {
                            tobeItem.tag(ProcessType.NO_CHANGE);
                        }
                        if (!asisItem.getValue().isEmpty()) {
                            asisItem.tag(ProcessType.UNSET);
                        } else {
                            asisItem.tag(ProcessType.NO_CHANGE);
                        }
                    }
                    continue next;
                }
            }
            tobeItem.tag(ProcessType.SET);
        }

        next: for(SpecificationItem asisItem: asisGroup.specificationItems) {
            for(SpecificationItem tobeItem: tobeGroup.specificationItems) {
                if(Objects.equals(asisItem.getName(), tobeItem.getName())) {
                    continue next;
                }
            }
            asisItem.tag(ProcessType.UNSET);
        }
    }

    public void addItem(SpecificationItem specificationItem) {
        this.specificationItems.add(specificationItem);
    }

    public void addLinkedGroup(SpecificationItemGroup opposite) {
        this.linkedSpecificationItemGroups.add(opposite);
    }

    public void tag(ProcessType type) {
        for(SpecificationItem item: this.specificationItems) {
            item.tag(type);
        }
    }

    public String getIdentifier() {
        return this.identifier;
    }

    public boolean isSameAs(SpecificationItemGroup oppositeGroup) {
        if(this.specificationItems.size() != oppositeGroup.specificationItems.size()) {
            return false;
        }

        next: for(SpecificationItem thisItem: this.specificationItems) {
            for(SpecificationItem oppositeItem: oppositeGroup.specificationItems) {
                if(Objects.equals(thisItem.getName(), oppositeItem.getName())
                        && Objects.equals(thisItem.getValue(), oppositeItem.getValue())) {
                    continue next;
                }
            }
            return false;
        }
        return true;
    }

    public String getMetaClassName() {
        return this.metaClassName;
    }

    public List<SpecificationItem> getSpecificationItems() {
        return this.specificationItems;
    }

    public List<SpecificationItemGroup> getLinkedSpecificationItemGroups() {
        return this.linkedSpecificationItemGroups;
    }

    public SpecificationItem searchItem(String itemName) {
        for(SpecificationItem item: this.specificationItems) {
            if(Objects.equals(item.getName(), itemName)) {
                return item;
            }
        }
        return null;
    }

    public void tagWithoutEmptyValue(ProcessType type) {
        for(SpecificationItem item: this.specificationItems) {
            if(!item.getValue().isEmpty()) {
                item.tag(type);
            } else {
                item.tag(ProcessType.NO_CHANGE);
            }
        }
    }
}
