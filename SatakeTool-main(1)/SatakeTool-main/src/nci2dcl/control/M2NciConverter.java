package nci2dcl.control;

import com.change_vision.jude.api.inf.AstahAPI;
import com.change_vision.jude.api.inf.model.*;
import com.change_vision.jude.api.inf.project.ProjectAccessor;
import nci2dcl.entity.nci.NetworkConfigurationInformation;
import nci2dcl.entity.nci.SpecificationItem;
import nci2dcl.entity.nci.SpecificationItemGroup;

import java.util.HashMap;
import java.util.Map;
import java.util.logging.Logger;

public class M2NciConverter {
    public static NetworkConfigurationInformation convert(String modelFilePath) {
        NetworkConfigurationInformation networkConfigurationInformation = new NetworkConfigurationInformation();
        try {
            AstahAPI api = AstahAPI.getAstahAPI();
            ProjectAccessor accessor = api.getProjectAccessor();
            accessor.open(modelFilePath, true, false, true);

            //Specification Item Group
            Map<IInstanceSpecification, SpecificationItemGroup> groupMap = new HashMap<>();
            for(INamedElement element: accessor.findElements(IInstanceSpecification.class)) {
                IInstanceSpecification instance = (IInstanceSpecification) element;
                SpecificationItemGroup group = new SpecificationItemGroup(instance.getName(), instance.getClassifier().getName());
                //Specification Item
                for(ISlot slot: instance.getAllSlots()) {
                    group.addItem(new SpecificationItem(slot.getName(), slot.getValue()));
                }
                groupMap.put(instance, group);
                networkConfigurationInformation.addGroup(group);
            }

            //Specification Item Group Relationship
            for(INamedElement element: accessor.findElements(ILink.class)) {
                ILink link = (ILink) element;

                if(link.getMemberEnds().length != 2) { // Assuming the number of link ends is always two.
                    Logger.getAnonymousLogger().warning("~~~~~~~Link MemberEnds != 2~~~~~~~~");
                    continue;
                }

                SpecificationItemGroup one = groupMap.get(link.getMemberEnds()[0].getType());
                SpecificationItemGroup other = groupMap.get(link.getMemberEnds()[1].getType());

                one.addLinkedGroup(other);
                if(one != other) { //avoid duplicated self-association
                    other.addLinkedGroup(one);
                }
            }

            accessor.close();
        } catch (Exception e) {
            throw
                    new IllegalStateException(e);
        }

        return networkConfigurationInformation;
    }
}
