package nci2dcl.entity.nci;

import java.util.HashSet;
import java.util.Objects;
import java.util.Set;

public enum ProcessType {
    NO_CHECK("no_check"),
    SET("set"),
    UNSET("unset"),
    NO_CHANGE("no_change");

    private final String label;
    ProcessType(String label) {
        this.label = label;
    }

    public static ProcessType parse(String typeString) {
        switch (ProcessType.getValueWithLabel(typeString.toLowerCase())) {
            case SET:
                return SET;
            case UNSET:
                return UNSET;
            case NO_CHANGE:
                return NO_CHANGE;
        }
        return NO_CHECK;
    }

    private static ProcessType getValueWithLabel(String typeString) {
        for(ProcessType differenceType: ProcessType.values()) {
            if(Objects.equals(differenceType.label, typeString)) {
                return differenceType;
            }
        }
        return NO_CHECK;
    }
}
