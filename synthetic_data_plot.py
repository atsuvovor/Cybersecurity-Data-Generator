def normalize_numerical_features(p_df):
    scaler = MinMaxScaler()
    p_df_daily = p_df.copy()
    df_normalized = pd.DataFrame(scaler.fit_transform(p_df_daily), columns=p_df_daily.columns.to_list(), index=p_df_daily.index)
    return df_normalized


#------------------------------------------------------------------
def plot_numerical_features_daily_values(df, date_column, feature_columns, rows, cols):

    fig, axes = plt.subplots(rows, cols, figsize=(16, 8))
    axes = axes.flatten()  # Flatten the 2D array of axes for easier iteration

    for i, column in enumerate(feature_columns):
        ax = axes[i]
        ax.plot(df.index, df[column], marker='o', label=column, color='b')
        ax.set_title(column, fontsize=10)
        ax.set_xlabel("Date Reported", fontsize=8)
        ax.set_ylabel(column, fontsize=8)
        ax.grid(True)
        ax.legend(fontsize=8)

        # Format x-axis to prevent overlapping
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=100))  # Show every 100 days
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right", fontsize=8)

    # Hide any unused subplots
    for j in range(len(feature_columns), len(axes)):
        axes[j].set_visible(False)

    plt.tight_layout()
    plt.show()


#------------------------------------------------------------------

def daily_distribution_of_activity_features_pipeline(df):
    """
    Pipeline to plot daily distribution of numerical features.
    """
    features = df.columns.tolist()
    n_features = len(features)
    rows = int(n_features/4)
    cols =  int(n_features/2)

    print("Non normalized daily distribution")
    plot_numerical_features_daily_values(df, "Date Reported", features, rows, cols)
    #plot_numerical_features_daily_values(df)
    print("Normalized daily distribution")
    df_normalized = normalize_numerical_features(df)
    #plot_numerical_features_daily_values(df_normalized)
    plot_numerical_features_daily_values(df_normalized, "Date Reported", features, rows, cols)
#-------------------------------------------------------------------------

def plot_histograms(df):
    """
    Plots histograms for all features in the list with risk level and displays basic statistics.
    """
    # Define the risk palette
    risk_palette = {
                    'Low': 'green',
                    'Medium': 'yellow',
                    'High': 'orange',
                    'Critical': 'red'
                   }

    features = df.columns.tolist()
    n_features = len(features)
    n_cols = int(n_features/2)
    n_rows = int((n_features + n_cols - 1) // n_cols)  # Calculate rows needed for the grid

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(5 * n_cols, n_rows * 6))  # Dynamically adjust figure size
    axes = np.array(axes)  # Ensure `axes` is always an array
    axes = axes.flatten()  # Flatten to handle indexing consistently

    for i, feature in enumerate(features):
        #sns.histplot(df[feature], bins=30, kde=True, ax=axes[i])
        if df[feature].dtype == 'object' and set(df[feature].unique()).issubset(risk_palette.keys()):
            sns.histplot(df[feature], palette=risk_palette, ax=axes[i])
        else:
            sns.histplot(df[feature], bins=30, kde=True, ax=axes[i])

        axes[i].set_title(f'Histogram of {feature}')
        axes[i].set_xlabel(feature)
        axes[i].set_ylabel('Frequency')

        # Calculate and display statistics for numeric features
        if np.issubdtype(df[feature].dtype, np.number):
            mean_return = df[feature].mean()
            std_dev = df[feature].std()
            skewness = df[feature].skew()
            kurtosis = df[feature].kurtosis()

            # Calculate and display statistics for numeric features
        if np.issubdtype(df[feature].dtype, np.number):
            statistics = (f"Mean: {mean_return:.4f}\n"
                      f"Std Dev: {std_dev:.4f}\n"
                      f"Skewness: {skewness:.4f}\n"
                      f"Kurtosis: {kurtosis:.4f}")
            axes[i].text(0.35, -0.18, statistics, transform=axes[i].transAxes,
                     fontsize=10, verticalalignment='top',
                     bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="lightgrey"))


    # Hide any unused subplots
    for j in range(n_features, len(axes)):
        axes[j].set_visible(False)

    #plt.tight_layout()
    plt.tight_layout(rect=[0, 0.05, 1, 1])  # Add padding to the bottom
    plt.show()

def plot_boxplots(df):
    """
    Plots boxplots for all features in the list and displays basic statistics.
    """
    # Define the risk palette
    risk_palette = {
                    'Low': 'green',
                    'Medium': 'yellow',
                    'High': 'orange',
                    'Critical': 'red'
                   }

    features  = df.columns.tolist()
    n_features = len(features)
    n_cols = int(n_features/2)
    n_rows = int((n_features + n_cols - 1) // n_cols)  # Calculate rows needed for the grid

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(5 * n_cols, n_rows * 6))  # Dynamically adjust figure size
    axes = np.array(axes)  # Ensure `axes` is always an array
    axes = axes.flatten()  # Flatten to handle indexing consistently

    for i, feature in enumerate(features):
        #sns.boxplot(y=df[feature], ax=axes[i])
        # Check if the feature has risk levels
        if df[feature].dtype == 'object' and set(df[feature].unique()).issubset(risk_palette.keys()):
            sns.boxplot(y=df[feature], palette=risk_palette, ax=axes[i])
        else:
            sns.boxplot(y=df[feature], ax=axes[i])

        axes[i].set_title(f'Boxplot of {feature}')
        axes[i].set_ylabel(feature)

        # Calculate and display statistics for numeric features
        if np.issubdtype(df[feature].dtype, np.number):
            mean_return = df[feature].mean()
            std_dev = df[feature].std()
            skewness = df[feature].skew()
            kurtosis = df[feature].kurtosis()

            # Add statistics below the plot
            statistics = (f"Mean: {mean_return:.4f}\n"
                      f"Std Dev: {std_dev:.4f}\n"
                      f"Skewness: {skewness:.4f}\n"
                      f"Kurtosis: {kurtosis:.4f}")
            axes[i].text(0.35, -0.18, statistics, transform=axes[i].transAxes,
                     fontsize=10, verticalalignment='top',
                     bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="lightgrey"))

    # Hide any unused subplots
    for j in range(n_features, len(axes)):
        axes[j].set_visible(False)

    #plt.tight_layout()
    plt.tight_layout(rect=[0, 0.05, 1, 1])  # Add padding to the bottom
    plt.show()
#-----------------------------------------------------------------------------------------------------

def visualize_form_of_activity_features_distribution(df):
    """
    Master function to plot histograms and boxplots for all features, with statistics.
    """
    sns.set(style="whitegrid")
    print("Plotting histograms...")
    plot_histograms(df)

    print("Plotting boxplots...")
    plot_boxplots(df)


def plot_scatter(axes, x, y, hue, df, palette, title, xlabel, ylabel, legend_title, ax_index):
    """
    Creates a scatter plot on the specified axis.
    """
    sns.scatterplot(x=x, y=y, hue=hue, data=df, palette=palette, ax=axes[ax_index])
    axes[ax_index].set_title(title)
    axes[ax_index].set_xlabel(xlabel)
    axes[ax_index].set_ylabel(ylabel)
    axes[ax_index].legend(title=legend_title)

def plot_correlation_heatmap(axes, df, features, ax_index):
    """
    Creates a heatmap showing the correlation between selected features.
    """
    # Select only numerical features
    numeric_features = df[features].select_dtypes(include=['number'])

     # Calculate the correlation matrix
    corr_matrix = numeric_features.corr()

    # Plot the heatmap
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar=True, ax=axes[ax_index])
    axes[ax_index].set_title("Correlation Heatmap of Numerical Features")

    #sns.heatmap(df[features].corr(), annot=True, cmap="coolwarm", fmt=".2f", ax=axes[ax_index])
    #axes[ax_index].set_title("Correlation Heatmap")


def combines_user_activities_scatter_plots_and_heatmap(scatter_df, df):
    """
    Combines scatter plots and heatmap into a single figure using subplots.
    """
    fig, axes = plt.subplots(1, 3, figsize=(24, 8))  # Create subplots (1 row, 3 columns)

    # Plot 1: Session Duration vs Data Transfer
    plot_scatter(
        axes=axes,
        x="Session Duration in Second",
        y="Data Transfer MB",
        hue="User Location",
        df=scatter_df,
        palette="Set1",
        title="Session Duration vs Data Transfer (MB) by Location",
        xlabel="Session Duration (seconds)",
        ylabel="Data Transfer (MB)",
        legend_title="User Location",
        ax_index=0
    )

    # Plot 2: Login Attempts vs Data Transfer
    plot_scatter(
        axes=axes,
        x="Login Attempts",
        y="Data Transfer MB",
        hue="User Location",
        df=scatter_df,
        palette="Set2",
        title="Login Attempts vs Data Transfer (MB) by Location",
        xlabel="Login Attempts",
        ylabel="Data Transfer (MB)",
        legend_title="User Location",
        ax_index=1
    )

    # Plot 3: Correlation Heatmap
    plot_correlation_heatmap(
        axes=axes,
        df=df,
        features=df.columns,
        ax_index=2
    )

    # Adjust layout and show plot
    plt.tight_layout()
    plt.show()

#-----------------------------------------Main EDA pipeline------------------------------------------------------
def explaratory_data_analysis_pipeline(df=None):

    if df is None:
        file_path_to_normal_and_anomalous_google_drive = \
                        "/content/drive/My Drive/Cybersecurity Data/normal_and_anomalous_cybersecurity_dataset_for_google_drive_kb.csv"

    eda_features =  [
    "Date Reported", "Issue Response Time Days", "Impact Score", "Cost",
    "Session Duration in Second", "Num Files Accessed", "Login Attempts",
    "Data Transfer MB", "CPU Usage %", "Memory Usage MB", "Threat Score"
    ]

    activity_features = [
    "Risk Level", "Threat Level", "Issue Response Time Days", "Impact Score", "Cost",
    "Session Duration in Second", "Num Files Accessed", "Login Attempts",
    "Data Transfer MB", "CPU Usage %", "Memory Usage MB", "Threat Score"
    ]
    #load real_world_simulated_normal_and_anomalous_df
    df = pd.read_csv(file_path_to_normal_and_anomalous_google_drive)

    reporting_frequency = 'Quarter'
    frequency = reporting_frequency[0].upper()
    if reporting_frequency.capitalize() == 'Month' or reporting_frequency.capitalize() == 'Quarter':
        frequency_date_column = reporting_frequency.capitalize() + '_Year'

    frequency_date_column = reporting_frequency.capitalize() + '_Year'
    eda_features_df = df[eda_features].copy()
    eda_features_df = eda_features_df.set_index("Date Reported")

    freq_eda_features_df = eda_features_df.copy()

    freq_eda_features_df[frequency_date_column] = pd.to_datetime(freq_eda_features_df.index)
    freq_eda_features_df[frequency_date_column] =  freq_eda_features_df[frequency_date_column].dt.to_period(frequency)

    freq_eda_features_df = freq_eda_features_df.groupby(frequency_date_column).mean()
    #df['Date Reported'] = df['Date Reported'].dt.to_timestamp()
    freq_eda_features_df.index = freq_eda_features_df.index.to_timestamp()
    display(freq_eda_features_df)


    activity_features_df = df[activity_features].copy()

    scatter_plot_features_df = df[["Session Duration in Second", "Login Attempts",
                                  "Data Transfer MB", "User Location"]].copy()

    #daily_distribution_of_activity_features_pipeline(eda_features_df )
    daily_distribution_of_activity_features_pipeline(freq_eda_features_df )
    visualize_form_of_activity_features_distribution(activity_features_df)
    combines_user_activities_scatter_plots_and_heatmap(scatter_plot_features_df, activity_features_df)
    return freq_eda_features_df

if __name__ == "__main__":

    real_world_normal_and_anomalous_df = explaratory_data_analysis_pipeline()