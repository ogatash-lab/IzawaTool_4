package nci2dcl.entity.nci;

public class SpecificationItem {
    private String name;
    private String value;
    private ProcessType processType = ProcessType.NO_CHECK;

    public SpecificationItem(String name, String value) {
        this.name = name;
        this.value = value;
    }

    public String getName() {
        return this.name;
    }

    public String getValue() {
        return this.value;
    }

    public ProcessType getProcessType() {
        return this.processType;
    }

    public void tag(ProcessType type) {
        this.processType = type;
    }
}
