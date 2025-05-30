package nci2dcl.entity.template;

import java.util.Objects;

public enum CommandTemplateFragmentType {
    NO_PROCESS(""),
    HEADER("header"),
    TEMPLATE("template"),
    FOOTER("footer"),
    MODE_BEFORE("mode_before"),
    MODE_AFTER("mode_after");

    private final String label;

    CommandTemplateFragmentType(String label) {
        this.label = label;
    }

    public static CommandTemplateFragmentType parse(String commandType) {
        for (CommandTemplateFragmentType type : CommandTemplateFragmentType.values()) {
            if (Objects.equals(commandType.toLowerCase(), type.label)) {
                return type;
            }
        }
        return NO_PROCESS;
    }
}
