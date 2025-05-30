package nci2dcl.entity.command;


import java.util.LinkedHashMap;
import java.util.Map;

public class CommandLists {
    private Map<String, CommandList> configCommandListMap = new LinkedHashMap<>();

    public Map<String, CommandList> getConfigCommandListMap() {
        return configCommandListMap;
    }

    public void put(String configName, CommandList commandList) {
        configCommandListMap.put(configName, commandList);
    }
}
