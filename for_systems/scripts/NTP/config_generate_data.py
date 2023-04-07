config = {
    "scheduler_config": {
        'gpu': ['0'],
        'temp_folder': 'temp',
        'scheduler_log_file_path': 'scheduler.log',
        'log_file': 'worker.log',
        'config_string_value_maxlen': 1000,
        'ignored_keys_for_folder_name': [
            'input_definition_file',
            'rpc_server_ip',
            'rpc_server_port',
            'regular_expression_file',
            'num_warm_ups',
            'random_order',
            'num_measurements',
            'averaging_method',
            'dataset_folder',
            'num_pre_warm_ups',
            'target_threshold_reference_dataset_folder',
            'synthetic_data_config',
            'dns_server_ip',
            'ntp_server_ip',
            'tree_file']
    },

    "global_config": {
        'batch_size': 100,
        'z_dim': 100,

        'gen_lr': 1e-3,
        'gen_beta1': 0.5,
        'disc_lr': 1e-3,
        'disc_beta1': 0.5,
        'disc_gp_coe': 10.0,

        'gen_num_layers': 6,
        'gen_l_dim': 600,
        'disc_num_shared_layers': 5,
        'disc_num_disc_layers': 1,
        'disc_num_class_layers': 1,
        'disc_l_dim': 600,

        'extra_iteration_checkpoint_freq': 10000,
        'iteration_log_freq': 10000,

        'class_loss_with_fake': True,
        'bal_class_weights': False,

        'num_generated_samples': 500000,
    },

    "test_config": [
        {
            'method': ['raregan'],
            'blackbox': ['ntp'],
            'bgt': [200000],
            'run': [0, 1, 2, 3, 4],

            'ini_rnd_bgt': [100000],
            'bgt_per_step': [100000],
            'oversampling_ratio': [10],

            'tgt_thld': [5.0, 10.0, 15.0, 20.0],
            'high_frc_mul': [3.0],

            'bal_disc_weights': [True],
            'num_iters_per_step': [100000],
            'disc_disc_coe': [1.0],
            'gen_disc_coe': [1.0],

            'input_definition_file': ['input_definitions/ntp_normal_input_definition.json'],
            'ntp_server_ip': ['127.0.0.1'],
        },
        {
            'method': ['raregan'],
            'blackbox': ['ntp'],
            'bgt': [100000],
            'run': [0, 1, 2, 3, 4],

            'ini_rnd_bgt': [50000],
            'bgt_per_step': [50000],
            'oversampling_ratio': [10],

            'tgt_thld': [10.0],
            'high_frc_mul': [3.0],

            'bal_disc_weights': [True],
            'num_iters_per_step': [100000],
            'disc_disc_coe': [1.0],
            'gen_disc_coe': [1.0],

            'input_definition_file': ['input_definitions/ntp_normal_input_definition.json'],
            'ntp_server_ip': ['127.0.0.1'],
        },
        {
            'method': ['raregan'],
            'blackbox': ['ntp'],
            'bgt': [50000],
            'run': [0, 1, 2, 3, 4],

            'ini_rnd_bgt': [25000],
            'bgt_per_step': [25000],
            'oversampling_ratio': [10],

            'tgt_thld': [10.0],
            'high_frc_mul': [3.0],

            'bal_disc_weights': [True],
            'num_iters_per_step': [100000],
            'disc_disc_coe': [1.0],
            'gen_disc_coe': [1.0],

            'input_definition_file': ['input_definitions/ntp_normal_input_definition.json'],
            'ntp_server_ip': ['<FILL IN IP ADDRESS>'],
        },
        {
            'method': ['raregan'],
            'blackbox': ['ntp'],
            'bgt': [20000],
            'run': [0, 1, 2, 3, 4],

            'ini_rnd_bgt': [10000],
            'bgt_per_step': [10000],
            'oversampling_ratio': [10],

            'tgt_thld': [10.0],
            'high_frc_mul': [3.0],

            'bal_disc_weights': [True],
            'num_iters_per_step': [100000],
            'disc_disc_coe': [1.0],
            'gen_disc_coe': [1.0],

            'input_definition_file': ['input_definitions/ntp_normal_input_definition.json'],
            'ntp_server_ip': ['<FILL IN IP ADDRESS>'],
        }
    ]
}
