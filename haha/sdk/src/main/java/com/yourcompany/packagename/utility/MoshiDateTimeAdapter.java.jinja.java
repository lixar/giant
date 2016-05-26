{% import 'variables.jinja' as vars with context %}
{% import 'variables-android.jinja' as android with context %}

{{ (android.main_path + '/utility/MoshiDateTimeAdapter')|start_of_file -}}
package {{ android.package_root_name }}.utility;

import com.squareup.moshi.FromJson;
import com.squareup.moshi.ToJson;

import org.threeten.bp.OffsetDateTime;

public class MoshiDateTimeAdapter {

    @ToJson
    String toJson(OffsetDateTime dateTime) {
        return dateTime.toString();
    }

    @FromJson
    OffsetDateTime fromJson(String dateTime) {
        return OffsetDateTime.parse(dateTime);
    }
}