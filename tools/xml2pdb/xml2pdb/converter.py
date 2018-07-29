from jinja2 import Environment, FileSystemLoader, StrictUndefined

import xml.etree.ElementTree as ET

import base64
import shutil
import os


def encode_pt(parameter_type):
    parameter_type = parameter_type.replace(" ", ".20")
    parameter_type = parameter_type.replace("_", ".5F")

    return parameter_type


def indent(elem, level=0):
    i = "\n" + level * "  "

    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def add_translations(languages_xml, items_xml, unit_id, element_id, tag_name):
    for itemXML in items_xml:
        countryCode = itemXML.get("{http://www.w3.org/XML/1998/namespace}lang")

        if countryCode is None:
            continue

        translation = itemXML.text
        language_xml = languages_xml.find(
            "*[@Identifier='" + countryCode + "']")

        if language_xml is None:
            language_xml = ET.SubElement(languages_xml, "Language")
            language_xml.set("Identifier", countryCode)

        translation_unit_xml = language_xml.find("*[@RefId='" + unit_id + "']")

        if translation_unit_xml is None:
            translation_unit_xml = ET.SubElement(
                language_xml, "TranslationUnit")
            translation_unit_xml.set("RefId", unit_id)

        translation_element_xml = translation_unit_xml.find(
            "*[@RefId='" + element_id + "']")

        if translation_element_xml is None:
            translation_element_xml = ET.SubElement(
                translation_unit_xml, "TranslationElement")
            translation_element_xml.set("RefId", element_id)

        translationXML = ET.SubElement(translation_element_xml, "Translation")
        translationXML.set("AttributeName", tag_name)
        translationXML.set("Text", translation)

    return

memory_segment_mapping = {}
com_object_idx = 0
com_object_ref_idx = 0
parameter_block_idx = 0
channel_idx = -1


def add_com_object(srcEntryXML, channelXML, comObjectTableXML, comObjectRefsXML,
                   master_root, knxns, application_program_id, languagesXML):
    global com_object_idx, com_object_ref_idx

    datapointTypeXML = master_root.find(
        ".//knx:DatapointSubtype[@Id='" +
        srcEntryXML.find("datapointType").text +
        "']/../..",
        knxns)
    datapointSubtypeXML = master_root.find(
        ".//knx:DatapointSubtype[@Id='" +
        srcEntryXML.find("datapointType").text +
        "']",
        knxns)

    bitSize = int(datapointTypeXML.get("SizeInBit"))

    if bitSize < 8:
        objectSize = "%d Bit" % bitSize
    elif bitSize == 8:
        objectSize = "1 Byte"
    elif (bitSize % 8) == 0:
        objectSize = "%d Bytes" % (bitSize / 8)
    else:
        raise ValueError(f"Unknown bitsize: {bitSize} bits")

    com_object_idx += 1
    comObjectId = application_program_id + "_O-%d" % com_object_idx
    comObjectXML = ET.SubElement(comObjectTableXML, "ComObject")
    comObjectXML.set("Id", comObjectId)
    comObjectXML.set("Name", srcEntryXML.get("name"))
    comObjectXML.set("Text", srcEntryXML.find("text").text)
    add_translations(
        languagesXML,
        srcEntryXML.findall("text"),
        application_program_id,
        comObjectId,
        "Text")
    comObjectXML.set("Number", str(com_object_idx))
    comObjectXML.set("FunctionText", srcEntryXML.find("function").text)
    add_translations(
        languagesXML,
        srcEntryXML.findall("function"),
        application_program_id,
        comObjectId,
        "FunctionText")
    comObjectXML.set("Priority", "Low")
    comObjectXML.set("ObjectSize", objectSize)

    comObjectXML.set("CommunicationFlag", "Enabled")

    if srcEntryXML.find("readFlag") is None:
        comObjectXML.set("ReadFlag", "Disabled")
    else:
        comObjectXML.set("ReadFlag", "Enabled")

    if srcEntryXML.find("writeFlag") is None:
        comObjectXML.set("WriteFlag", "Disabled")
    else:
        comObjectXML.set("WriteFlag", "Enabled")

    if srcEntryXML.find("transmitFlag") is None:
        comObjectXML.set("TransmitFlag", "Disabled")
    else:
        comObjectXML.set("TransmitFlag", "Enabled")

    if srcEntryXML.find("updateFlag") is None:
        comObjectXML.set("UpdateFlag", "Disabled")
    else:
        comObjectXML.set("UpdateFlag", "Enabled")

    if srcEntryXML.find("readOnInitFlag") is None:
        comObjectXML.set("ReadOnInitFlag", "Disabled")
    else:
        comObjectXML.set("ReadOnInitFlag", "Enabled")

    comObjectXML.set(
        "DatapointType",
        srcEntryXML.find("datapointType").text)
    # Not in spec. Obsolete? comObjectXML.set("VisibleDescription", "")

    com_object_ref_idx += 1
    comObjectRefId = comObjectId + "_R-%d" % com_object_ref_idx
    comObjectRefXML = ET.SubElement(comObjectRefsXML, "ComObjectRef")
    comObjectRefXML.set("Id", comObjectRefId)
    comObjectRefXML.set("RefId", comObjectId)
    # According to spec: Name. Missing?
    # According to spec: Text. Missing?
    # According to spec: Function Text. Missing?
    # According to spec: Priority. Missing?
    # According to spec: Object Size. Missing?
    # According to spec: Read Flag. Missing?
    # According to spec: Write Flag. Missing?
    # According to spec: Communication Flag. Missing?
    # According to spec: Transmit Flag. Missing?
    # According to spec: Update Flag. Missing?
    # According to spec: ReadOnInit Flag. Missing?
    #comObjectRefXML.set("DatapointType", "DPST-10-1")
    comObjectRefXML.set("Tag", str(com_object_ref_idx))

    comObjectRefRefXML = ET.SubElement(channelXML, "ComObjectRefRef")
    comObjectRefRefXML.set("RefId", comObjectRefId)


def add_parameter_block(parent_xml, name, application_program_id):
    global parameter_block_idx

    parameter_block_idx += 1
    parameterBlockId = application_program_id + "_PB-%d" % parameter_block_idx
    parameterBlockXML = ET.SubElement(parent_xml, "ParameterBlock")
    parameterBlockXML.set("Id", parameterBlockId)
    parameterBlockXML.set("Name", name)
    parameterBlockXML.set("Text", name)
    # According to spec: Access. Missing?
    # According to spec: Help Topic ID. Missing?

    return parameterBlockXML


def add_channel(parent_xml, name, application_program_id):
    global channel_idx

    channel_idx += 1
    channelId = application_program_id + "_CH-%d" % channel_idx
    channelXML = ET.SubElement(parent_xml, "Channel")
    channelXML.set("Id", channelId)
    channelXML.set("Name", name)
    channelXML.set("Text", name)
    channelXML.set("Number", str(channel_idx))

    return channelXML


def add_memory_segment(parent_xml, application_program_id, address, size, name,
                       data=None, mask=None):
    id = application_program_id + "_AS-" + "%04X" % int(address)

    memory_segment_xml = ET.SubElement(parent_xml, "AbsoluteSegment")

    memory_segment_xml.set("Id", id)
    memory_segment_xml.set("Address", address)
    memory_segment_xml.set("Size", size)

    if data is not None:
        ET.SubElement(memory_segment_xml, "Data").text = data

    if mask is not None:
        ET.SubElement(memory_segment_xml, "Mask").text = mask

    if name is not None:
        memory_segment_mapping[name] = id

    return memory_segment_xml


def create_root_node():
    rootXML = ET.Element("KNX")

    rootXML.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
    rootXML.set("xmlns:xsd", "http://www.w3.org/2001/XMLSchema")
    rootXML.set("CreatedBy", "knxconv")
    rootXML.set("ToolVersion", "4.0.1907.45562")
    rootXML.set("xmlns", "http://knx.org/xml/project/13")

    return rootXML


def create_catalog(srcRootXML, manufacturer_id, catalog_section_id, catalog_number, catalog_item_id, catalog_item_number, product_id, hardware_program_id):
    languagesXML = ET.Element("Languages")
    src_device_xml = srcRootXML.find("info")
    dstRootXML = create_root_node()

    manufacturerDataXML = ET.SubElement(dstRootXML, "ManufacturerData")

    manufacturerXML = ET.SubElement(manufacturerDataXML, "Manufacturer")
    manufacturerXML.set("RefId", manufacturer_id)

    catalogXML = ET.SubElement(manufacturerXML, "Catalog")

    catalogSectionXML = ET.SubElement(catalogXML, "CatalogSection")
    catalogSectionXML.set("Id", catalog_section_id)
    catalogSectionXML.set("Name", src_device_xml.find("category").text)
    add_translations(
        languagesXML,
        src_device_xml.findall("category"),
        catalog_section_id,
        catalog_section_id,
        "Name")
    catalogSectionXML.set("Number", catalog_number)
    catalogSectionXML.set("VisibleDescription", "")
    catalogSectionXML.set("DefaultLanguage", "de-DE")
    catalogSectionXML.set("NonRegRelevantDataVersion", "0")

    catalogItemXML = ET.SubElement(catalogSectionXML, "CatalogItem")
    catalogItemXML.set("Id", catalog_item_id)
    catalogItemXML.set("Name", src_device_xml.find("name").text)
    add_translations(
        languagesXML,
        src_device_xml.findall("name"),
        catalog_item_id,
        catalog_item_id,
        "Name")
    catalogItemXML.set("Number", catalog_item_number)
    # According to spec: VisibleDescription. Missing?
    catalogItemXML.set("ProductRefId", product_id)
    catalogItemXML.set("Hardware2ProgramRefId", hardware_program_id)
    catalogItemXML.set("DefaultLanguage", "de-DE")
    catalogItemXML.set("NonRegRelevantDataVersion", "0")

    manufacturerXML.append(languagesXML)

    return dstRootXML


def create_hardware(srcRootXML, manufacturer_id, hardware_id, serial_number, version_number, product_id, order_number, hardware_program_id, application_program_id):
    languagesXML = ET.Element("Languages")
    src_device_xml = srcRootXML.find("info")
    dstRootXML = create_root_node()

    manufacturerDataXML = ET.SubElement(dstRootXML, "ManufacturerData")

    manufacturerXML = ET.SubElement(manufacturerDataXML, "Manufacturer")
    manufacturerXML.set("RefId", manufacturer_id)

    hardwaresXML = ET.SubElement(manufacturerXML, "Hardware")

    hardwareXML = ET.SubElement(hardwaresXML, "Hardware")
    hardwareXML.set("Id", hardware_id)
    hardwareXML.set("Name", src_device_xml.find("name").text)
    hardwareXML.set("SerialNumber", serial_number)
    hardwareXML.set("VersionNumber", version_number)
    hardwareXML.set("BusCurrent", "12")
    hardwareXML.set("IsAccessory", "0")
    hardwareXML.set("HasIndividualAddress", "1")
    hardwareXML.set("HasApplicationProgram", "1")
    # According to spec: Download Application Program. Missing?
    hardwareXML.set("HasApplicationProgram2", "0")
    # According to spec: Download Application Program2. Missing?
    hardwareXML.set("IsPowerSupply", "0")
    hardwareXML.set("IsChoke", "0")
    hardwareXML.set("IsCoupler", "0")
    hardwareXML.set("IsPowerLineRepeater", "0")
    hardwareXML.set("IsPowerLineSignalFilter", "0")
    hardwareXML.set("IsCable", "0")
    hardwareXML.set("NonRegRelevantDataVersion", "0")
    hardwareXML.set("IsIPEnabled", "0")

    productsXML = ET.SubElement(hardwareXML, "Products")

    productXML = ET.SubElement(productsXML, "Product")
    productXML.set("Id", product_id)
    productXML.set("Text", src_device_xml.find("name").text)
    add_translations(
        languagesXML,
        src_device_xml.findall("name"),
        product_id,
        product_id,
        "Name")
    productXML.set("OrderNumber", order_number)
    productXML.set("IsRailMounted", "1")
    productXML.set("WidthInMillimeter", "1.0500000e+002")
    productXML.set("VisibleDescription", src_device_xml.find("name").text)
    add_translations(
        languagesXML,
        src_device_xml.findall("name"),
        product_id,
        product_id,
        "VisibleDescription")
    productXML.set("DefaultLanguage", "de-DE")
    productXML.set("Hash", "")
    productXML.set("NonRegRelevantDataVersion", "0")

    registrationInfoXML = ET.SubElement(productXML, "RegistrationInfo")
    registrationInfoXML.set("RegistrationStatus", "Registered")
    registrationInfoXML.set("RegistrationSignature", "")

    hardware2ProgramsXML = ET.SubElement(hardwareXML, "Hardware2Programs")

    hardware2ProgramXML = ET.SubElement(
        hardware2ProgramsXML, "Hardware2Program")
    hardware2ProgramXML.set("Id", hardware_program_id)
    hardware2ProgramXML.set("MediumTypes", "MT-0")
    hardware2ProgramXML.set("Hash", "")

    applicationProgramRefXML = ET.SubElement(
        hardware2ProgramXML, "ApplicationProgramRef")
    applicationProgramRefXML.set("RefId", application_program_id)

    # According to spec: Application Program 2 Ref. Missing?

    registrationInfoXML = ET.SubElement(
        hardware2ProgramXML, "RegistrationInfo")
    registrationInfoXML.set("RegistrationStatus", "Registered")
    registrationInfoXML.set("RegistrationSignature", "")

    manufacturerXML.append(languagesXML)

    return dstRootXML


def create_product(master_root, srcRootXML, manufacturer_id, application_program_id, application_number, application_version, knxns):
    languagesXML = ET.Element("Languages")
    src_device_xml = srcRootXML.find("info")
    dstRootXML = create_root_node()

    load_procedure_style_xml = src_device_xml.find("loadProcedureStyle")
    load_procedure_style = load_procedure_style_xml.text \
        if load_procedure_style_xml else "DefaultProcedure"

    manufacturerDataXML = ET.SubElement(dstRootXML, "ManufacturerData")

    manufacturerXML = ET.SubElement(manufacturerDataXML, "Manufacturer")
    manufacturerXML.set("RefId", manufacturer_id)

    applicationProgramsXML = ET.SubElement(
        manufacturerXML, "ApplicationPrograms")

    applicationProgramXML = ET.SubElement(
        applicationProgramsXML, "ApplicationProgram")
    applicationProgramXML.set("Id", application_program_id)
    applicationProgramXML.set("ApplicationNumber", application_number)
    applicationProgramXML.set("ApplicationVersion", application_version)
    applicationProgramXML.set("ProgramType", "ApplicationProgram")
    applicationProgramXML.set("MaskVersion", "MV-0705")
    # According to spec: Visible Description. Missing?
    applicationProgramXML.set("Name", src_device_xml.find("name").text)
    add_translations(
        languagesXML,
        src_device_xml.findall("name"),
        application_program_id,
        application_program_id,
        "Name")
    applicationProgramXML.set("LoadProcedureStyle", load_procedure_style)
    applicationProgramXML.set("PeiType", "0")
    # According to spec: Serial Number. Missing?
    # According to spec: Help Topic ID. Missing?
    applicationProgramXML.set("HelpFile", "")
    applicationProgramXML.set("DefaultLanguage", "de-DE")
    applicationProgramXML.set("DynamicTableManagement", "0")
    applicationProgramXML.set("Linkable", "0")
    applicationProgramXML.set("MinEtsVersion", "4.0")
    applicationProgramXML.set("PreEts4Style", "0")
    applicationProgramXML.set("NonRegRelevantDataVersion", "0")
    # According to spec: Replaces Versions. Missing?
    applicationProgramXML.set("Hash", "")
    # Not in spec. Obsolete? applicationProgramXML.set("ConvertedFromPreEts4Data", "1")
    # Not in spec. Obsolete? applicationProgramXML.set("Broken", "0")
    applicationProgramXML.set("IPConfig", "Tool")
    applicationProgramXML.set("AdditionalAddressesCount", "0")
    # Not in spec. Obsolete? applicationProgramXML.set("DownloadInfoIncomplete", "0")
    # Not in spec. Obsolete?
    # applicationProgramXML.set("CreatedFromLegacySchemaVersion", "0")

    staticXML = ET.SubElement(applicationProgramXML, "Static")

    codeXML = ET.SubElement(staticXML, "Code")
    parameterTypesXML = ET.SubElement(staticXML, "ParameterTypes")
    parametersXML = ET.SubElement(staticXML, "Parameters")
    parameterRefsXML = ET.SubElement(staticXML, "ParameterRefs")
    comObjectTableXML = ET.SubElement(staticXML, "ComObjectTable")
    comObjectRefsXML = ET.SubElement(staticXML, "ComObjectRefs")
    addressTableXML = ET.SubElement(staticXML, "AddressTable")
    associationTableXML = ET.SubElement(staticXML, "AssociationTable")
    loadProceduresXML = ET.SubElement(staticXML, "LoadProcedures")
    extensionXML = ET.SubElement(staticXML, "Extension")
    optionsXML = ET.SubElement(staticXML, "Options")

    dynamicXML = ET.SubElement(applicationProgramXML, "Dynamic")

    #
    # Memory segments
    #
    src_memory_segments_xml = srcRootXML.find("memorySegments")

    for src_memory_segment_xml in src_memory_segments_xml:
        data_xml = src_memory_segment_xml.find("data")
        mask_xml = src_memory_segment_xml.find("mask")

        memory_segment_xml = add_memory_segment(
            codeXML, application_program_id,
            src_memory_segment_xml.get("address"),
            src_memory_segment_xml.get("size"),
            src_memory_segment_xml.get("name"),
            data=data_xml.text if data_xml is not None else None,
            mask=mask_xml.text if mask_xml is not None else None)

        # Set reference to the different tables.
        if src_memory_segment_xml.get("name") == "AddressTable":
            addressTableXML.set("CodeSegment", memory_segment_xml.get("Id"))
            addressTableXML.set("Offset", "0")
            addressTableXML.set(
                "MaxEntries", str(int(src_memory_segment_xml.get("size")) // 3))
        elif src_memory_segment_xml.get("name") == "AssocTable":
            associationTableXML.set(
                "CodeSegment", memory_segment_xml.get("Id"))
            associationTableXML.set("Offset", "0")
            associationTableXML.set(
                "MaxEntries", str(int(src_memory_segment_xml.get("size")) // 3))
        elif src_memory_segment_xml.get("name") == "ComObjectTable":
            comObjectTableXML.set("CodeSegment", memory_segment_xml.get("Id"))
            comObjectTableXML.set("Offset", "0")

    srcChannelsXML = srcRootXML.find("channels")
    parameterIdx = 0
    parameterSeparatorIdx = 0

    channelIndependentBlockXML = ET.SubElement(
        dynamicXML, "ChannelIndependentBlock")

    for srcChannelXML in srcChannelsXML:
        if srcChannelXML.tag == "channel":
            channelXML = add_channel(
                dynamicXML,
                srcChannelXML.find("name").text,
                application_program_id)
            add_translations(
                languagesXML,
                srcChannelXML.findall("name"),
                application_program_id,
                channelXML.get("Id"),
                "Text")
        elif srcChannelXML.tag == "channelIndependent":
            channelXML = channelIndependentBlockXML
        else:
            raise Exception(f"Unsupported tag: {srcChannelXML.tag}")

        srcParameterBlocksXML = srcChannelXML.find("parameterBlocks")

        for srcParameterBlockXML in srcParameterBlocksXML:
            parameterBlockXML = add_parameter_block(
                channelXML,
                srcParameterBlockXML.find("name").text,
                application_program_id)
            add_translations(
                languagesXML,
                srcParameterBlockXML.findall("name"),
                application_program_id,
                parameterBlockXML.get("Id"),
                "Text")

            srcParametersXML = srcParameterBlockXML.find("parameters")

            for srcEntryXML in srcParametersXML:
                if srcEntryXML.tag == "parameter":
                    parameterTypeName = srcEntryXML.get("name")
                    parameterTypeId = application_program_id + \
                        "_PT-" + encode_pt(parameterTypeName)
                    parameterTypeXML = ET.SubElement(
                        parameterTypesXML, "ParameterType")
                    parameterTypeXML.set("Id", parameterTypeId)
                    parameterTypeXML.set("Name", parameterTypeName)
                    parameterTypeXML.set("Plugin", "")

                    type = srcEntryXML.get("type")

                    if (type == "unsignedInt") | (type == "signedInt"):
                        sizeInBit = srcEntryXML.get("sizeInBit")

                        typeNumberXML = ET.SubElement(
                            parameterTypeXML, "TypeNumber")
                        typeNumberXML.set("SizeInBit", sizeInBit)

                        minInclusive = srcEntryXML.get("minInclusive")
                        maxInclusive = srcEntryXML.get("maxInclusive")

                        if (type == "unsignedInt"):
                            if minInclusive is None:
                                minInclusive = "0"

                            if maxInclusive is None:
                                maxInclusive = str((1 << int(sizeInBit)) - 1)

                            typeNumberXML.set("Type", "unsignedInt")
                        else:
                            if minInclusive is None:
                                minInclusive = "-" + \
                                    str(1 << (int(sizeInBit) - 1))

                            if maxInclusive is None:
                                maxInclusive = str(
                                    (1 << (int(sizeInBit) - 1)) - 1)

                            typeNumberXML.set("Type", "signedInt")

                        typeNumberXML.set("minInclusive", minInclusive)
                        typeNumberXML.set("maxInclusive", maxInclusive)

                        if srcEntryXML.get("uiHint") is not None:
                            typeNumberXML.set(
                                "UIHint", srcEntryXML.get("uiHint"))
                    elif type == "float":
                        typeFloatXML = ET.SubElement(
                            parameterTypeXML, "TypeFloat")

                        sizeInBit = srcEntryXML.get("sizeInBit")
                        minInclusive = srcEntryXML.get("minInclusive")
                        maxInclusive = srcEntryXML.get("maxInclusive")

                        if sizeInBit == "16":
                            encoding = "DPT 9"

                            if minInclusive is None:
                                minInclusive = "-671088.64"

                            if maxInclusive is None:
                                maxInclusive = "670760.96"

                        elif sizeInBit == "32":
                            encoding = "IEEE-754 Single"

                            if minInclusive is None:
                                minInclusive = "1.175e-38"

                            if maxInclusive is None:
                                maxInclusive = "3.4028235e+38"

                        elif sizeInBit == "64":
                            encoding = "IEEE-754 Double"

                            if minInclusive is None:
                                minInclusive = "2.2251e-308"

                            if maxInclusive is None:
                                maxInclusive = "1.798e308"
                        else:
                            raise ValueError(f"Unkown sizeInBit: {sizeInBit}")

                        typeFloatXML.set("Encoding", encoding)
                        typeFloatXML.set("minInclusive", minInclusive)
                        typeFloatXML.set("maxInclusive", maxInclusive)

                        if srcEntryXML.get("uiHint") is not None:
                            typeFloatXML.set(
                                "UIHint", srcEntryXML.get("uiHint"))
                    elif type == "text":
                        typeTextXML = ET.SubElement(
                            parameterTypeXML, "TypeText")
                        typeTextXML.set(
                            "SizeInBit", srcEntryXML.get("sizeInBit"))

                        if srcEntryXML.get("pattern") is not None:
                            typeTextXML.set(
                                "Pattern", srcEntryXML.get("pattern"))
                    elif type == "enumeration":
                        typeRestrictionXML = ET.SubElement(
                            parameterTypeXML, "TypeRestriction")
                        typeRestrictionXML.set("Base", "Value")
                        typeRestrictionXML.set(
                            "SizeInBit", srcEntryXML.get("sizeInBit"))

                        srcEntriesXML = srcEntryXML.find("entries")

                        for srcListEntryXML in srcEntriesXML:
                            enumerationValue = srcListEntryXML.get("value")
                            enumerationId = parameterTypeId + "_EN-%s" % enumerationValue
                            enumerationXML = ET.SubElement(
                                typeRestrictionXML, "Enumeration")
                            enumerationXML.set("Id", enumerationId)
                            # Obsolete! enumerationXML.set("DisplayOrder", "")
                            enumerationXML.set(
                                "Text", srcListEntryXML.find("name").text)
                            add_translations(languagesXML, srcListEntryXML.findall(
                                "name"), application_program_id, enumerationId, "Text")
                            enumerationXML.set("Value", enumerationValue)
                    else:
                        raise ValueError(f"Unsupported type: {type}")

                    parameterIdx = parameterIdx + 1
                    parameterId = application_program_id + "_P-%d" % parameterIdx
                    parameterXML = ET.SubElement(parametersXML, "Parameter")
                    parameterXML.set("Id", parameterId)
                    parameterXML.set("Name", srcEntryXML.get("name"))
                    parameterXML.set("ParameterType", parameterTypeId)
                    parameterXML.set("Text", srcEntryXML.find("text").text)
                    add_translations(
                        languagesXML,
                        srcEntryXML.findall("text"),
                        application_program_id,
                        parameterId,
                        "Text")
                    # According to spec: SuffixText. Missing?
                    parameterXML.set("Access", "ReadWrite")
                    parameterXML.set("Value", srcEntryXML.get("default"))
                    # According to spec: Patch Always. Missing?
                    # According to spec: Unique Number. Missing?

                    src_memory_xml = srcEntryXML.find("memory")

                    if src_memory_xml is not None:

                        segment = src_memory_xml.get("segment")
                        memory_segment_id = memory_segment_mapping[segment]

                        memoryXML = ET.SubElement(parameterXML, "Memory")
                        memoryXML.set("CodeSegment", memory_segment_id)
                        memoryXML.set("Offset", src_memory_xml.get("offset"))
                        memoryXML.set("BitOffset", "0")

                    #propertyXML = ET.SubElement(parameterXML, "Property")
                    #propertyXML.set("ObjectIndex", "0")
                    #propertyXML.set("PropertyId", "0")
                    #propertyXML.set("Offset", "0")
                    #propertyXML.set("BitOffset", "0")

                    parameterRefId = parameterId + "_R-1"
                    parameterRefXML = ET.SubElement(
                        parameterRefsXML, "ParameterRef")
                    parameterRefXML.set("Id", parameterRefId)
                    parameterRefXML.set("RefId", parameterId)
                    # According to spec: Text. Missing?
                    # According to spec: SuffixText. Missing?
                    # Obsolete! parameterRefXML.set("DisplayOrder", "1")
                    # According to spec: Access. Missing?
                    # According to spec: Default Value. Missing?
                    parameterRefXML.set("Tag", "1")

                    parameterRefRefXML = ET.SubElement(
                        parameterBlockXML, "ParameterRefRef")
                    parameterRefRefXML.set("RefId", parameterRefId)

                elif srcEntryXML.tag == "parameterSeparator":
                    parameterSeparatorIdx += + 1
                    parameterSeparatorId = application_program_id + "_PS-%d" % parameterSeparatorIdx
                    parameterSeparatorXML = ET.SubElement(
                        parameterBlockXML, "ParameterSeparator")
                    parameterSeparatorXML.set("Id", parameterSeparatorId)
                    parameterSeparatorText = srcEntryXML.find("text")
                    if parameterSeparatorText is None:
                        parameterSeparatorXML.set("Text", "")
                    else:
                        parameterSeparatorXML.set(
                            "Text", srcEntryXML.find("text").text)
                        add_translations(
                            languagesXML,
                            srcEntryXML.findall("text"),
                            application_program_id,
                            parameterSeparatorId,
                            "Text")
                    # According to spec: Access. Missing?

                else:
                    raise ValueError(f"Unknown tag: {srcEntryXML.tag}")

            srcComObjectsXML = srcParameterBlockXML.find("comObjects") or []

            for srcComObjectXML in srcComObjectsXML:
                if srcComObjectXML.tag == "comObject":
                    add_com_object(
                        srcComObjectXML, parameterBlockXML,
                        comObjectTableXML, comObjectRefsXML,
                        master_root, knxns, application_program_id,
                        languagesXML)

    optionsXML.set(
        "TextParameterEncodingSelector",
        "UseTextParameterEncodingCodePage")
    optionsXML.set("TextParameterEncoding", "utf-8")

    #chooseXML = ET.SubElement(parameterBlockXML, "choose")
    #chooseXML.set("ParamRefId", parameterRefId)

    #whenXML = ET.SubElement(chooseXML, "when")
    #whenXML.set("test", "1")

    manufacturerXML.append(languagesXML)

    return dstRootXML


def create_environment():
    """
    Create a new Jinja2 render environment.
    """

    root_dir = os.path.join(os.path.dirname(__file__), "..")
    file_dir = os.path.abspath(os.path.dirname(__file__))
    environment = Environment(
        loader=FileSystemLoader([root_dir, file_dir, "/"]),
        undefined=StrictUndefined,
        keep_trailing_newline=True)

    environment.filters['b64decode'] = \
        lambda x: base64.b64decode(x.decode("ascii")).encode('ascii')
    environment.filters['b64encode'] = \
        lambda x: base64.b64encode(x.encode("ascii")).decode('ascii')

    return environment


def run(master_file, source_file, output_directory, context):
    """
    Main entry point for this utility.
    """

    # Parse the master file.
    master_tree = ET.parse(master_file)
    master_root = master_tree.getroot()
    knxns = {"knx": "http://knx.org/xml/project/14"}

    # Convert template into source
    with open(source_file, "r") as fp:
        source = create_environment().from_string(fp.read()).render(**context)

    tree = ET.fromstring(source)
    root = tree
    src_device_xml = root.find("info")

    manufacturer_id = src_device_xml.find("manufacturerId").text
    catalog_number = src_device_xml.find("catalogNumber").text
    catalog_item_number = src_device_xml.find("catalogItemNumber").text
    serial_number = src_device_xml.find("serialNumber").text
    version_number = src_device_xml.find("versionNumber").text
    order_number = src_device_xml.find("orderNumber").text
    application_number = src_device_xml.find("applicationNumber").text
    application_version = src_device_xml.find("applicationVersion").text

    catalog_section_id = manufacturer_id + "_CS-" + catalog_number
    hardware_id = manufacturer_id + "_H-" + serial_number + "-" + version_number
    product_id = hardware_id + "_P-" + order_number
    hardware_program_id = hardware_id + "_HP-" + \
        "%04X" % int(application_number) + "-" + \
        "%02X" % int(application_version) + "-F00D"
    application_program_id = manufacturer_id + "_A-" + \
        "%04X" % int(application_number) + "-" + \
        "%02X" % int(application_version) + "-F00D"
    catalog_item_id = hardware_program_id + "_CI-" + \
        order_number + "-" + catalog_item_number

    # Create the XML trees.
    catalog_xml = create_catalog(
        root, manufacturer_id, catalog_section_id, catalog_number,
        catalog_item_id, catalog_item_number, product_id, hardware_program_id)
    indent(catalog_xml)
    catalog_tree = ET.ElementTree(catalog_xml)

    hardware_xml = create_hardware(
        root, manufacturer_id, hardware_id, serial_number, version_number,
        product_id, order_number, hardware_program_id, application_program_id)
    indent(hardware_xml)
    hardware_tree = ET.ElementTree(hardware_xml)

    product_xml = create_product(
        master_root,
        root, manufacturer_id, application_program_id, application_number,
        application_version, knxns)
    indent(product_xml)
    product_tree = ET.ElementTree(product_xml)

    # Cleanup the old directory if needed and create a new one.
    if os.path.isdir(output_directory):
        shutil.rmtree(output_directory)

    os.makedirs(output_directory)
    os.makedirs(os.path.join(output_directory, manufacturer_id))

    # Write the files to the destination folder.
    shutil.copyfile(
        master_file, os.path.join(output_directory, "knx_master.xml"))

    catalog_tree.write(
        os.path.join(output_directory, manufacturer_id, "Catalog.xml"),
        "utf-8",
        True)
    hardware_tree.write(
        os.path.join(output_directory, manufacturer_id, "Hardware.xml"),
        "utf-8",
        True)
    product_tree.write(
        os.path.join(
            output_directory,
            manufacturer_id,
            application_program_id + ".xml"),
        "utf-8",
        True)
