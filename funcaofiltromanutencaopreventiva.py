def loadDevicesForMaintenance(self, filtering=False, filteringFields=None, start_index=0, end_index=20):
    """
    This method is called to load the call types from database
    """
    # --> object used to communicate with the database #
    myDBConnection = DBConnection()

    fields = [
        "dis_id",
        "dis_descricao",
        "dis_codigo_sap",
        "dis_cliente",
        "cli_nome",
        "nof_numero",
        "dis_status",
        "sdi_descricao",
        "dis_doc_enviado",
        "dis_com_imagem",
        "dis_extensao_imagem",
        "ese_numero_nota_fiscal_saida",
        "ese_id",
        "dis_com_manutencao",
        "dis_info_manutencao"
    ]

    tables = [
        ("dispositivos", "", ""),
        ("clientes", "LEFT", "dis_cliente = cli_id"),
        ("entrada_saida_equipamento", "LEFT", "dis_nota_fiscal_atual = ese_id"),
        ("notas_fiscais", "LEFT", "ese_nota_fiscal_entrada = nof_id"),
        ("status_dispositivo", "LEFT", "dis_status = sdi_id"),
        ("vinculacao_dispositivo_produto", "LEFT", "dis_id = vdp_dispositivo"),
        ("dispositivo_info_manutencao", "LEFT", "dis_info_manutencao = dim_id")
    ]

    if not filtering:
        where = ["vdp_id IS NOT NULL AND sdi_id = '2'"]
    else:
        filteringFields.append("vdp_id IS NOT NULL")
        where = filteringFields

    groupby = ["dis_id"]

    orderby = ["dis_id DESC"]

    # Apply pagination
    limit = [str(start_index) + ", " + str(end_index - start_index)]

    querySuccess, queryResult = myDBConnection.selectQuery(fields, tables, where, groupby, None, orderby, limit)

    if not querySuccess:
        raise DatabaseConnectionError("Durante o carregamento dos dispositivos.",
                                      "Falha ao tentar executar a consulta no banco.\nContate o administrador do sistema.")
        return

    self.clear()

    for (
            deviceId,
            deviceDescription,
            deviceSAPCode,
            deviceClientId,
            deviceClientName,
            deviceInvoiceNumber,
            deviceStatusId,
            deviceStatusDescription,
            deviceDocSent,
            deviceHasImage,
            deviceImageExtension,
            deviceOutInvoiceNumber,
            deviceInOutInvoiceId,
            deviceHasMaintenance,
            deviceInfoMaintenance
    ) in queryResult:
        device = Device(
            deviceId,
            deviceDescription,
            deviceSAPCode,
            deviceClientId,
            deviceClientName,
            deviceInvoiceNumber,
            deviceStatusId,
            deviceStatusDescription,
            deviceDocSent,
            deviceHasImage,
            deviceImageExtension,
            deviceOutInvoiceNumber,
            deviceInOutInvoiceId,
            deviceHasMaintenance,
            deviceInfoMaintenance
        )

        device.loadMaintenanceData()

        self.add(device)
