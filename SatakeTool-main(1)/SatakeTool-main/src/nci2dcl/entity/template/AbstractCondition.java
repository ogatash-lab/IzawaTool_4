package nci2dcl.entity.template;

import nci2dcl.entity.nci.ProcessType;
import nci2dcl.entity.nci.SpecificationItem;
import nci2dcl.entity.nci.SpecificationItemGroup;

import java.util.Locale;
import java.util.Objects;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class AbstractCondition {
    private static final Pattern conditionPattern = Pattern.compile("(<.+?>)\\s*==\\s*(.*?)\\s*");

    private String rawString = "";
    private String parameter = "";
    private String value = "";

    public AbstractCondition(String condition) {
        this.rawString = condition.trim();

        Matcher m = conditionPattern.matcher(condition);
        if(m.matches()) {
            this.parameter = m.group(1).trim();
            this.value = m.group(2).trim();
        }
    }

    @Override
    public String toString() {
        if(!parameter.isEmpty() || !value.isEmpty()) {
            return parameter + " == " + value;
        } else {
            return "";
        }

    }

    public boolean match(SpecificationItemGroup group) {
        if (this.rawString.isEmpty()) {
            return true;
        }

        SpecificationItem item = group.searchItem(deParameterize(this.parameter));
        if (item == null) {
            return true;
        }

        return Objects.equals(value.toLowerCase(), item.getValue().toLowerCase());
    }

    private String deParameterize(String parameter) {
        return parameter.replaceAll("[<>]", "");
    }
}
